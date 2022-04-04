from enum import Enum
import RPi.GPIO as GPIO
import time
from typing import Tuple


class Phase(Enum):
    ONE = 0
    TWO = 1
    THREE = 3
    FOUR = 4


class StepperMotor:
    """Class for cleanly controlling operation of DC stepper motor"""

    step_delay = 0.01

    def __init__(
            self,
            phase_a_pins: Tuple[int, int],
            phase_b_pins: Tuple[int, int]) -> None:
        """Initialize pins for stepper motor"""
        self.phase_a_pins = phase_a_pins
        self.phase_b_pins = phase_b_pins
        self.phase = Phase.ONE
        GPIO.setup(self.phase_a_pins[0], GPIO.OUT)
        GPIO.setup(self.phase_a_pins[1], GPIO.OUT)
        GPIO.setup(self.phase_b_pins[0], GPIO.OUT)
        GPIO.setup(self.phase_b_pins[1], GPIO.OUT)
        GPIO.output(self.phase_a_pins[0], GPIO.LOW)
        GPIO.output(self.phase_a_pins[1], GPIO.LOW)
        GPIO.output(self.phase_b_pins[0], GPIO.LOW)
        GPIO.output(self.phase_b_pins[1], GPIO.LOW)

    def reset_phase(self):
        """Resets the stepper motor phase to phase one"""
        self.phase = Phase.ONE

    def step_one_forward(self):
        """Turn the stepper motor one step forward based on current phase"""
        if self.phase == Phase.ONE:
            GPIO.output(self.phase_a_pins[0], GPIO.LOW)
            GPIO.output(self.phase_b_pins[1], GPIO.HIGH)
            self.phase = Phase.TWO
        elif self.phase == Phase.TWO:
            GPIO.output(self.phase_b_pins[1], GPIO.LOW)
            GPIO.output(self.phase_a_pins[1], GPIO.HIGH)
            self.phase = Phase.THREE
        elif self.phase == Phase.THREE:
            GPIO.output(self.phase_a_pins[1], GPIO.LOW)
            GPIO.output(self.phase_b_pins[0], GPIO.HIGH)
            self.phase = Phase.FOUR
        elif self.phase == Phase.FOUR:
            GPIO.output(self.phase_b_pins[0], GPIO.LOW)
            GPIO.output(self.phase_a_pins[0], GPIO.HIGH)
            self.phase == Phase.ONE
        time.sleep(self.step_delay)

    def step_forward(self, steps: int):
        """Turn the stepper motor forward the specified number of steps"""
        for _ in range(steps):
            self.step_one_forward()

    def step_one_backward(self):
        """Turn the stepper motor one step backward based on current phase"""
        if self.phase == Phase.ONE:
            GPIO.output(self.phase_a_pins[1], GPIO.LOW)
            GPIO.output(self.phase_b_pins[1], GPIO.HIGH)
            self.phase = Phase.TWO
        elif self.phase == Phase.TWO:
            GPIO.output(self.phase_b_pins[1], GPIO.LOW)
            GPIO.output(self.phase_a_pins[0], GPIO.HIGH)
            self.phase = Phase.THREE
        elif self.phase == Phase.THREE:
            GPIO.output(self.phase_a_pins[0], GPIO.LOW)
            GPIO.output(self.phase_b_pins[0], GPIO.HIGH)
            self.phase = Phase.FOUR
        elif self.phase == Phase.FOUR:
            GPIO.output(self.phase_b_pins[0], GPIO.LOW)
            GPIO.output(self.phase_a_pins[1], GPIO.HIGH)
            self.phase == Phase.ONE
        time.sleep(self.step_delay)

    def step_backward(self, steps: int):
        """Turn the stepper motor backward the specified number of steps"""
        for _ in range(steps):
            self.step_one_backward()
