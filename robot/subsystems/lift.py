from typing import Tuple

from robot.hardware.stepper_motor import StepperMotor


class Lift:
    """Class for cleanly controlling lift subsystem"""

    rise_steps: int = 1650
    increment_steps: int = 200
    clear_steps: int = 600
    lower_steps: int = 2000

    def __init__(
        self,
        phase_a_pins: Tuple[int, int],
        phase_b_pins: Tuple[int, int]
    ) -> None:
        """Initialize stepper motor for lift"""
        self.stepper = StepperMotor(phase_a_pins, phase_b_pins)

    def initial_rise(self) -> None:
        """Lift scissor lift to default height"""
        self.stepper.step_forward(self.rise_steps)

    def second_rise(self) -> None:
        """Lift scissor lift from run height to default height"""
        self.stepper.step_forward(
            self.lower_steps -
            self.increment_steps -
            self.clear_steps)

    def incremement(self) -> None:
        """Lift scissor lift an additional small amount"""
        self.stepper.step_forward(self.increment_steps)

    def clear(self) -> None:
        """Lift scissor lift to clear beads from hook"""
        self.stepper.step_forward(self.clear_steps)

    def lower(self) -> None:
        """Lower scissor lift to default height"""
        self.stepper.step_backward(self.lower_steps)

    def reset(self) -> None:
        """Lower scissor lift back to starting height"""
        self.stepper.step_backward(
            self.rise_steps +
            self.clear_steps +
            self.increment_steps -
            self.lower_steps)

    def stop(self) -> None:
        """Wrapper for resetting stepper motor phase"""
        self.stepper.reset_phase()
