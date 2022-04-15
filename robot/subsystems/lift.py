from typing import Tuple

from robot.hardware.stepper_motor import StepperMotor


class Lift:
    """Class for cleanly controlling lift subsystem"""

    rise_steps: int = 0
    lower_steps: int = 0

    def __init__(
        self,
        phase_a_pins: Tuple[int, int],
        phase_b_pins: Tuple[int, int]
    ) -> None:
        """Initialize stepper motor for lift"""
        self.stepper = StepperMotor(phase_a_pins, phase_b_pins)

    def rise(self) -> None:
        """Lift scissor lift to default height"""
        self.stepper.step_forward(self.rise_steps)

    def lower(self) -> None:
        """Lower scissor lift to default height"""
        self.stepper.step_backward(self.lower_steps)

    def reset(self) -> None:
        """Lower scissor lift back to starting height"""
        self.stepper.step_backward(self.rise_steps - self.lower_steps)

    def stop(self) -> None:
        self.stepper.reset_phase()
