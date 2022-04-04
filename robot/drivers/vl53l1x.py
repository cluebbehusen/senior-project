# The following code is adapted from Adafruit Industries code here:
# https://github.com/adafruit/Adafruit_CircuitPython_VL53L1X,
# licensed under MIT

import time
import struct
from adafruit_bus_device import i2c_device
from micropython import const

_VL53L1X_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND = const(0x0008)
_GPIO_HV_MUX__CTRL = const(0x0030)
_GPIO__TIO_HV_STATUS = const(0x0031)
_PHASECAL_CONFIG__TIMEOUT_MACROP = const(0x004B)
_RANGE_CONFIG__TIMEOUT_MACROP_A_HI = const(0x005E)
_RANGE_CONFIG__VCSEL_PERIOD_A = const(0x0060)
_RANGE_CONFIG__TIMEOUT_MACROP_B_HI = const(0x0061)
_RANGE_CONFIG__VCSEL_PERIOD_B = const(0x0063)
_RANGE_CONFIG__VALID_PHASE_HIGH = const(0x0069)
_SD_CONFIG__WOI_SD0 = const(0x0078)
_SD_CONFIG__INITIAL_PHASE_SD0 = const(0x007A)
_SYSTEM__INTERRUPT_CLEAR = const(0x0086)
_SYSTEM__MODE_START = const(0x0087)
_VL53L1X_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0 = const(0x0096)
_VL53L1X_IDENTIFICATION__MODEL_ID = const(0x010F)
_ADDRESS_REGISTER = const(0x0001)

_DEFAULT_ADDRESS = const(41)

TB_SHORT_DIST = {
    15: (b"\x00\x1D", b"\x00\x27"),
    20: (b"\x00\x51", b"\x00\x6E"),
    33: (b"\x00\xD6", b"\x00\x6E"),
    50: (b"\x01\xAE", b"\x01\xE8"),
    100: (b"\x02\xE1", b"\x03\x88"),
    200: (b"\x03\xE1", b"\x04\x96"),
    500: (b"\x05\x91", b"\x05\xC1"),
}

TB_LONG_DIST = {
    20: (b"\x00\x1E", b"\x00\x22"),
    33: (b"\x00\x60", b"\x00\x6E"),
    50: (b"\x00\xAD", b"\x00\xC6"),
    100: (b"\x01\xCC", b"\x01\xEA"),
    200: (b"\x02\xD9", b"\x02\xF8"),
    500: (b"\x04\x8F", b"\x04\xA4"),
}


class VL53L1X:
    """Driver for the VL53L1X distance sensor"""

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c, _DEFAULT_ADDRESS)
        model_id, module_type, mask_rev = self.model_info
        if model_id != 0xEA or module_type != 0xCC or mask_rev != 0x10:
            raise RuntimeError("[!] Wrong sensor ID or type")
        self._sensor_init()
        self._timing_budget = None
        self.timing_budget = 50
        if (address != _DEFAULT_ADDRESS):
            self._change_address(address)

    def _sensor_init(self):
        init_seq = bytes(
            [
                0x00, 0x00, 0x00, 0x01, 0x02, 0x00, 0x02, 0x08, 0x00, 0x08,
                0x10, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x0F,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x0B, 0x00, 0x00, 0x02,
                0x0A, 0x21, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0xC8,
                0x00, 0x00, 0x38, 0xFF, 0x01, 0x00, 0x08, 0x00, 0x00, 0x01,
                0xCC, 0x0F, 0x01, 0xF1, 0x0D, 0x01, 0x68, 0x00, 0x80, 0x08,
                0xB8, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x89, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x01, 0x0F, 0x0D, 0x0E, 0x0E, 0x00,
                0x00, 0x02, 0xC7, 0xFF, 0x9B, 0x00, 0x00, 0x00, 0x01, 0x00,
                0x00,
            ]
        )
        self._write_register(0x002D, init_seq)
        self.start_ranging()
        while not self.data_ready:
            time.sleep(0.01)
        self.clear_interrupt()
        self.stop_ranging()
        self._write_register(
            _VL53L1X_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND, b"\x09")
        self._write_register(0x0B, b"\x00")

    @property
    def model_info(self):
        """A tuple of Model ID, Module Type, and Mask Revision"""
        info = self._read_register(_VL53L1X_IDENTIFICATION__MODEL_ID, 3)
        return (info[0], info[1], info[2])  # Model ID, Module Type, Mask Rev

    @property
    def distance(self):
        """The distance in units of centimeter"""
        dist = self._read_register(
            _VL53L1X_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0, 2
        )
        dist = struct.unpack(">H", dist)[0]
        return dist / 10

    def start_ranging(self):
        """Starts ranging operation"""
        self._write_register(_SYSTEM__MODE_START, b"\x40")

    def stop_ranging(self):
        """Stops ranging operation"""
        self._write_register(_SYSTEM__MODE_START, b"\x00")

    def clear_interrupt(self):
        """Clears new data interrupt"""
        self._write_register(_SYSTEM__INTERRUPT_CLEAR, b"\x01")

    @property
    def data_ready(self):
        """Returns true if new data is ready, otherwise false"""
        if (
            self._read_register(_GPIO__TIO_HV_STATUS)[0] & 0x01
            == self._interrupt_polarity
        ):
            return True
        return False

    @property
    def timing_budget(self):
        """Ranging duration in milliseconds. Increasing the timing budget
        increases the maximum distance the device can range and improves
        the repeatability error. However, average power consumption augments
        accordingly. ms = 15 (short mode only), 20, 33, 50, 100, 200, 500"""
        return self._timing_budget

    @timing_budget.setter
    def timing_budget(self, val):
        reg_vals = None
        mode = self.distance_mode
        if mode == 1:
            reg_vals = TB_SHORT_DIST
        if mode == 2:
            reg_vals = TB_LONG_DIST
        if reg_vals is None:
            raise RuntimeError("[!] Unknown distance mode")
        if val not in reg_vals.keys():
            raise ValueError("[!] Invalid timing budget")
        self._write_register(
            _RANGE_CONFIG__TIMEOUT_MACROP_A_HI, reg_vals[val][0])
        self._write_register(
            _RANGE_CONFIG__TIMEOUT_MACROP_B_HI, reg_vals[val][1])
        self._timing_budget = val

    def _change_address(self, i2c, addr):
        self._write_register(_ADDRESS_REGISTER, addr.to_bytes(1, 'big'))
        self.i2c_device = i2c_device.I2CDevice(i2c, addr)
        time.sleep(0.01)

    @property
    def _interrupt_polarity(self):
        int_pol = self._read_register(_GPIO_HV_MUX__CTRL)[0] & 0x10
        int_pol = (int_pol >> 4) & 0x01
        return 0 if int_pol else 1

    @property
    def distance_mode(self):
        """The distance mode: 1=short, 2=long"""
        mode = self._read_register(_PHASECAL_CONFIG__TIMEOUT_MACROP)[0]
        if mode == 0x14:
            return 1  # short distance
        if mode == 0x0A:
            return 2  # long distance
        return None  # unknown

    @distance_mode.setter
    def distance_mode(self, mode):
        # short distance
        if mode == 1:
            self._write_register(_PHASECAL_CONFIG__TIMEOUT_MACROP, b"\x14")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_A, b"\x07")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_B, b"\x05")
            self._write_register(_RANGE_CONFIG__VALID_PHASE_HIGH, b"\x38")
            self._write_register(_SD_CONFIG__WOI_SD0, b"\x07\x05")
            self._write_register(_SD_CONFIG__INITIAL_PHASE_SD0, b"\x06\x06")
        # long distance
        elif mode == 2:
            self._write_register(_PHASECAL_CONFIG__TIMEOUT_MACROP, b"\x0A")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_A, b"\x0F")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_B, b"\x0D")
            self._write_register(_RANGE_CONFIG__VALID_PHASE_HIGH, b"\xB8")
            self._write_register(_SD_CONFIG__WOI_SD0, b"\x0F\x0D")
            self._write_register(_SD_CONFIG__INITIAL_PHASE_SD0, b"\x0E\x0E")
        else:
            raise ValueError("[!] Unsupported mode.")
        self.timing_budget = self._timing_budget

    def _write_register(self, address, data, length=None):
        if length is None:
            length = len(data)
        with self.i2c_device as i2c:
            i2c.write(struct.pack(">H", address) + data[:length])

    def _read_register(self, address, length=1):
        data = bytearray(length)
        with self.i2c_device as i2c:
            i2c.write(struct.pack(">H", address))
            i2c.readinto(data)
        return data
