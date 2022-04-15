from typing import Callable, Dict

from robot.subsystems.lift import Lift
from robot.states.state_types import (
    LiftInput,
    LiftOutput,
    LiftState
)


class LiftStateMachine():
    """State machine for managing control of robot scissor lift"""

    outputs: Dict[LiftState, LiftOutput] = {
        LiftState.REST: {
            'finish': True
        },
        LiftState.RAISE: {
            'finish': False
        },
        LiftState.INCREMENT: {
            'finish': False
        },
        LiftState.LOWER: {
            'finish': False
        },
        LiftState.RESET: {
            'finish': False
        }
    }

    def __init__(self, lift: Lift) -> None:
        """Initialize startin state and state transition dictionary"""
        self.state: LiftState = LiftState.REST
        self.transitions: Dict[LiftState, Callable[[LiftInput], None]] = {
            LiftState.REST: self.transition_from_rest,
            LiftState.RAISE: self.transition_from_raise,
            LiftState.LOWER: self.transition_from_lower,
            LiftState.RESET: self.transition_from_rest
        }
        self.lift = lift

    def transition(self, input: LiftInput) -> LiftOutput:
        """Perform transition and return output of new state"""
        self.transitions[self.state](input)
        return self.outputs[self.state]

    def transition_from_rest(self, input: LiftInput) -> None:
        """Transition from REST state to next state"""
        lift, increment, lower, reset = input['lift'], input['increment'], input['lower'], input['reset']
        if lift:
            self.state = LiftState.RAISE
        if increment:
            self.state = LiftState.INCREMENT
        elif lower:
            self.state = LiftState.LOWER
        elif reset:
            self.state = LiftState.RESET

    def transition_from_raise(self, input: LiftInput) -> None:
        """Transition from RAISE state to next state"""
        self.lift.rise()
        self.state = LiftState.REST

    def transition_from_increment(self, input: LiftInput) -> None:
        """Transition from INCREMENT state to next state"""
        self.lift.incremement()
        self.state = LiftState.REST

    def transition_from_lower(self, input: LiftInput) -> None:
        """Transition from LOWER state to next state"""
        self.lift.lower()
        self.state = LiftState.REST

    def transition_from_reset(self, input: LiftInput) -> None:
        """Transition from RESET state to next state"""
        self.lift.reset()
        self.state = LiftState.REST
