import pigpio
from typing import Type


class LinearActuator:
    """Class for cleanly controlling extension of Actuonix linear actuator"""

    def __init__(
            self,
            pi: Type[pigpio.pi],
            pwm_pin: int,
            frequency: int) -> None:
        """Initialize linear actuator with extension of 0"""
        self.pi = pi
        self.pwm_pin = pwm_pin
        self.pi.set_PWM_frequency(self.pwm_pin, frequency)
        self.pi.set_PWM_dutycycle(self.pwm_pin, 0)

    def set_extension_percent(self, percent: int) -> None:
        """Sets extension by a percent (0-100)"""
        if percent < 0 or percent > 100:
            return
        adj_pwm = int(percent * 255)
        self.pi.set_PWM_dutycycle(self.pwm_pin, adj_pwm)

    def set_extension_pwm(self, pwm: int) -> None:
        """Sets extension by a PWM (0-255)"""
        if pwm < 0 or pwm > 255:
            return
        self.pi.set_PWM_dutycycle(self.pwm_pin, pwm)

    def set_extension_minimum(self) -> None:
        """Retracts linear actuator completely"""
        self.pi.set_PWM_dutycycle(self.pwm_pin, 0)

    def set_extension_maximum(self) -> None:
        """Extends linear actuator completely"""
        self.pi.set_PWM_dutycycle(self.pwm_pin, 255)
