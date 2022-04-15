import pigpio
import time

from robot.hardware.brushed_motor import BrushedMotor
from robot.hardware.linear_actuator import LinearActuator


class Grabber:
    """Class for cleanly controlling grabber subsystem"""

    grab_initial_delay: float = 0.0
    grab_actuator_min_pwm: int = 0
    grab_actuator_max_pwm: int = 0
    grab_motor_pwm: int = 0
    grab_extension_delay: float = 0.0
    grab_end_delay: float = 0.0
    retract_delay: float = 0.0
    cup_distance: int = 0
    cup_extension_delay: float = 0.0
    dispense_pwm: int = 0
    dispense_time: float = 0.0

    def __init__(
            self,
            pi: pigpio.pi,
            linear_actuator_pwm_pin: int,
            brushed_motor_pwm_pin: int,
            brushed_motor_direction_pin: int) -> None:
        """Initialize linear actuator and brushed motor objects"""
        self.motor: BrushedMotor = BrushedMotor(
            pi,
            brushed_motor_direction_pin,
            brushed_motor_pwm_pin,
            1000)
        self.actuator: LinearActuator = LinearActuator(
            pi,
            linear_actuator_pwm_pin,
            1000
        )

    def grab(self) -> None:
        """Extend grabbing mechanism and grab beads"""
        self.motor.set_direction_forward()
        self.motor.set_motor_pwm(self.grab_motor_pwm)
        self.actuator.set_extension_pwm(self.grab_actuator_min_pwm)
        time.sleep(self.grab_initial_delay)
        for pwm in range(
                self.grab_actuator_min_pwm,
                self.grab_actuator_max_pwm):
            self.actuator.set_extension_pwm(pwm)
            time.sleep(self.grab_extension_delay)
        time.sleep(self.grab_end_delay)
        self.motor.set_motor_pwm(0)

    def retract(self) -> None:
        """Retract grabbing mechanism"""
        self.actuator.set_extension_minimum()
        time.sleep(self.retract_delay)

    def extend_to_cup(self) -> None:
        """Extend grabbing mechanism to hover over cup"""
        self.actuator.set_extension_percent(self.cup_distance)
        time.sleep(self.cup_extension_delay)

    def dispense_beads(self) -> None:
        """Rotate grabbing mechanism to drop beads"""
        self.motor.set_direction_backward()
        self.motor.set_motor_pwm(self.dispense_pwm)
        time.sleep(self.dispense_time)
        self.motor.set_motor_pwm(0)
        self.motor.set_direction_forward()

    def stop(self) -> None:
        self.actuator.set_extension_minimum()
        self.motor.set_motor_pwm(0)
