from board import I2C
from typing import Type
from robot.drivers.vl53l1x import VL53L1X


class TOF:
    """Class for cleaning interacting with a single time-of-flight sensor"""

    def __init__(self, i2c: Type[I2C], address: int) -> None:
        """Initialize VL53L1X sensor"""
        self.device = VL53L1X(i2c, address)
    
    def get_distance(self) -> float:
        """Get and return distance reading of sensor"""
        return self.device.distance
    
