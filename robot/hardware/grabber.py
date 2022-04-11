import pigpio
import time
from typing import Type

from robot.hardware.brushed_motor import BrushedMotor
from robot.hardware.linear_actuator import LinearActuator


class Grabber:
    """Class for cleanly controlling grabber subsystem"""

    cup_distance: int = 0
    cup_extension_time: float = 0.0
    dispense_pwm: int = 0
    dispense_time: float = 0.0

    def __init__(
            self,
            pi: Type[pigpio.pi],
            linear_actuator_pwm_pin: int,
            brushed_motor_pwm_pin: int,
            brushed_motor_direction_pin: int) -> None:
        """Initialize linear actuator and brushed motor objects"""
        self.motor = BrushedMotor(
            pi,
            brushed_motor_direction_pin,
            brushed_motor_pwm_pin,
            1000)
        self.actuator = LinearActuator(
            pi,
            linear_actuator_pwm_pin,
            1000
        )

    def grab(self):
        """Extend grabbing mechanism and grab beads"""
        pass

    def retract(self) -> None:
        """Retract grabbing mechanism"""
        self.actuator.set_extension_minimum()

    def extend_to_cup(self) -> None:
        """Extend grabbing mechanism to hover over cup"""
        self.actuator.set_extension_percent(self.cup_distance)
        time.sleep(self.cup_extension_time)

    def dispense_beads(self) -> None:
        """Rotate grabbing mechanism to drop beads"""
        self.motor.set_direction_backward()
        self.motor.set_motor_pwm(self.dispense_pwm)
        time.sleep(self.dispense_time)
        self.motor.set_motor_pwm(0)
        self.motor.set_direction_forward()
