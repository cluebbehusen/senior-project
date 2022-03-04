from board import I2C
from statistics import mean
from typing import Type

from robot.drivers.vl53l1x import VL53L1X


class TOF:
    """Class for cleaning interacting with a single time-of-flight sensor"""

    def __init__(self, i2c: Type[I2C], address: int) -> None:
        """Initialize VL53L1X sensor"""
        self.device = VL53L1X(i2c, address)
        self.device.distance_mode = 2
        self.device.timing_budget = 100
        self.device.start_ranging()
        self.distances = []

    def get_distance(self) -> float:
        """Get and return distance reading of sensor"""
        if self.device.data_ready:
            if len(self.distances) == 10:
                self.distances.pop()
            self.distances.append(self.device.distance)
        if len(self.distances) != 0:
            return mean(self.distances)
        return 0
