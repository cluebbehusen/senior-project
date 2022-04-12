import pigpio
import time

from robot.hardware.brushed_motor import BrushedMotor


class Launcher:
    """Class for cleanly controlling launcher subsystem"""

    run_end_delay: float = 0.0
    motor_frequency: int = 10000

    def __init__(
        self,
        pi: pigpio.pi,
        brushed_motor_pwm_pin: int,
        brushed_motor_direction_pin: int,
    ) -> None:
        """Initialize brushed motor object for launcher"""
        self.motor: BrushedMotor = BrushedMotor(
            pi,
            brushed_motor_pwm_pin,
            brushed_motor_direction_pin,
            self.motor_frequency
        )

    def run(self) -> None:
        """Start launcher belt spinning"""
        self.motor.set_direction_forward()
        self.motor.set_motor_pwm(255)

    def stop(self) -> None:
        """Stop launcher belt spinning"""
        time.sleep(self.run_end_delay)
        self.motor.set_motor_pwm(0)
