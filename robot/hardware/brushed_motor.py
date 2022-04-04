import pigpio
import RPi.GPIO as GPIO
from typing import Type, Union


class BrushedMotor:
    """Class for cleanly controlling speed and direction of brushed DC motor"""

    def __init__(
            self,
            pi: Type[pigpio.pi],
            direction_pin: int,
            pwm_pin: int,
            frequency: int) -> None:
        """Initialize brushed motor with forward direction and speed of 0"""
        self.pi = pi
        self.direction_pin = direction_pin
        self.pwm_pin = pwm_pin
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.output(self.direction_pin, GPIO.LOW)
        self.pi.set_PWM_frequency(self.pwm_pin, frequency)
        self.pi.set_PWM_dutycycle(self.pwm_pin, 0)

    def set_direction(self, direction: Union[GPIO.LOW, GPIO.HIGH]) -> None:
        """Change direction to the given direction"""
        GPIO.output(self.direction_pin, direction)

    def set_direction_forward(self) -> None:
        """Change direction to forward"""
        GPIO.output(self.direction_pin, GPIO.LOW)

    def set_direction_backward(self) -> None:
        """Change direction to backward"""
        GPIO.output(self.direction_pin, GPIO.HIGH)

    def set_motor_pwm(self, pwm: int) -> None:
        """Change duty cycle of motor"""
        self.pi.set_PWM_dutycycle(self.pwm_pin, pwm)

    def set_pwm_frequency(self, frequency: int) -> None:
        """Change PWM frequency of motor"""
        self.pi.set_PWM_frequency(self.pwm_pin, frequency)
