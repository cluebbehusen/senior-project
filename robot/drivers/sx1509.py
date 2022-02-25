from adafruit_bus_device import i2c_device
from micropython import const

# Pin types
PIN_TYPE_INPUT = const(0x00)
PIN_TYPE_OUTPUT = const(0x01)
PIN_TYPE_INPUT_PULLUP = const(0x02)
PIN_TYPE_ANALOG_OUTPUT = const(0x03)
PIN_TYPE_INPUT_PULLDOWN = const(0x04)
PIN_TYPE_INPUT_OPEN_DRAIN = const(0x05)

# Interrupt states
INTERRUPT_STATE_CHANGE = const(0b11)
INTERRUPT_STATE_FALLING = const(0b10)
INTERRUPT_STATE_RISING = const(0b01)

_SX1509_RegPullUpB = const(0x06)
_SX1509_RegPullDownB = const(0x08)
_SX1509_RegOpenDrainB = const(0x0A)
_SX1509_RegDirB = const(0x0E)
_SX1509_RegDataB = const(0x10)

_SX1509_RegReset = const(0x7D)


class SX1509:

    def __init__(self, i2c, address=0x3E):
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        self.reset()

    def reset(self):
        self._write_reg_8(_SX1509_RegReset, 0x12)
        self._write_reg_8(_SX1509_RegReset, 0x34)

    def pinMode(self, pin, input_mode):
        mode_bit = 1
        if (input_mode == PIN_TYPE_OUTPUT) or (input_mode == PIN_TYPE_ANALOG_OUTPUT):
            mode_bit = 0

        tempRegDir = self._read_reg_16(_SX1509_RegDirB)
        if mode_bit == 1:
            tempRegDir |= (1 << pin)
        else:
            tempRegDir &= ~(1 << pin)

        self._write_reg_16(_SX1509_RegDirB, tempRegDir)

        self.setInputMode(pin, input_mode)

    def setInputMode(self, pin, input_mode):
        tempRegData = self._read_reg_16(_SX1509_RegPullUpB)
        tempRegData &= ~(1 << pin)
        self._write_reg_16(_SX1509_RegPullUpB, tempRegData)

        tempRegData = self._read_reg_16(_SX1509_RegPullDownB)
        tempRegData &= ~(1 << pin)
        self._write_reg_16(_SX1509_RegPullDownB, tempRegData)

        tempRegData = self._read_reg_16(_SX1509_RegOpenDrainB)
        tempRegData &= ~(1 << pin)
        self._write_reg_16(_SX1509_RegOpenDrainB, tempRegData)

        if input_mode == PIN_TYPE_INPUT_PULLUP:
            tempRegData = self._read_reg_16(_SX1509_RegPullUpB)
            tempRegData |= (1 << pin)
            self._write_reg_16(_SX1509_RegPullUpB, tempRegData)
        elif input_mode == PIN_TYPE_INPUT_PULLDOWN:
            tempRegData = self._read_reg_16(_SX1509_RegPullDownB)
            tempRegData |= (1 << pin)
            self._write_reg_16(_SX1509_RegPullDownB, tempRegData)
        elif (input_mode == PIN_TYPE_INPUT_OPEN_DRAIN) or (input_mode == PIN_TYPE_ANALOG_OUTPUT):
            tempRegData = self._read_reg_16(_SX1509_RegOpenDrainB)
            tempRegData |= (1 << pin)
            self._write_reg_16(_SX1509_RegOpenDrainB, tempRegData)

    def digitalWrite(self, pin, highLow):
        tempRegDir = self._read_reg_16(_SX1509_RegDirB)

        # pin is output, write high/low
        if (0xFFFF ^ tempRegDir) & (1 << pin):
            tempRegData = self._read_reg_16(_SX1509_RegDataB)
            if (highLow == 1):
                tempRegData |= (1 << pin)
            else:
                tempRegData &= ~(1 << pin)
            self._write_reg_16(_SX1509_RegDataB, tempRegData)

        # pin is input, pull-up/pull-down
        else:
            tempPullUp = self._read_reg_16(_SX1509_RegPullUpB)
            tempPullDown = self._read_reg_16(_SX1509_RegPullDownB)

            if (highLow == 1):  # if HIGH, do pull-up, disable pull-down
                tempPullUp |= (1 << pin)
                tempPullDown &= ~(1 << pin)
                self._write_reg_16(_SX1509_RegPullDownB, tempPullDown)
                self._write_reg_16(_SX1509_RegPullUpB, tempPullUp)
            else:  # If LOW do pull-down, disable pull-up
                tempPullDown |= (1 << pin)
                tempPullUp &= ~(1 << pin)
                self._write_reg_16(_SX1509_RegPullUpB, tempPullUp)
                self._write_reg_16(_SX1509_RegPullDownB, tempPullDown)

    def digitalRead(self, pin):
        tempRegDir = self._read_reg_16(_SX1509_RegDirB)

        if (tempRegDir & (1 << pin)):  # if the pin is an input
            tempRegData = self._read_reg_16(_SX1509_RegDataB)
            if (tempRegData & (1 << pin)):
                return 1
        # return 0 if pin is low or pin is output
        return 0

    def _write_reg_8(self, reg, val):
        self.i2c_device.write(bytes([reg, val]))

    def _write_reg_16(self, reg, val):
        self.i2c_device.write(
            bytes([reg, ((val >> 8) & (0xFF)), (val & 0xFF)]))

    def _read_reg_8(self, reg):
        self.i2c_device.write(bytes([reg]))
        result = bytearray(1)
        self.i2c_device.readinto(result)
        return result[0]

    def _read_reg_16(self, reg):
        self.i2c_device.write(bytes([reg]))
        result = bytearray(2)
        self.i2c_device.readinto(result)
        return ((result[0] << 8) | result[1])
