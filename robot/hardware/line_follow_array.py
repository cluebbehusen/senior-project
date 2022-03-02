from board import I2C
from typing import List, Tuple, Type
from robot.drivers.sx1509 import SX1509, PIN_TYPE_INPUT


class LineFollowArray:
    """Class for cleanly interacting with line following sensor array"""

    multiplier_values = [1, 2, 3, 4]

    def __init__(self, i2c: Type[I2C], pins: List[int]) -> None:
        """Initialize all 8 sensors on the I2C breakout"""
        self.device = SX1509(i2c)
        self.pins = pins
        for pin in pins:
            self.device.pinMode(pin, PIN_TYPE_INPUT)

    def read_sensors(self) -> List[int]:
        """Read binary values from all 8 sensors"""
        readings = []
        for pin in self.pins:
            readings.append(self.device.digitalRead(pin))
        return readings

    def get_sensor_reading_magnitude(self) -> Tuple[int, int]:
        """Get equivalent magnitude value for binary list reading"""
        readings = self.read_sensors()
        leftSum = 0
        rightSum = 0
        for index, reading in enumerate(readings[3::-1]):
            leftSum += reading * self.multiplier_values[index]
        for index, reading in enumerate(readings[4:]):
            rightSum += reading * self.multiplier_values[index]
        return (leftSum, rightSum)
