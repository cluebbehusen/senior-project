from typing import Callable, Dict

from robot.subsystems.grabber import Grabber
from robot.states.state_types import (
    GrabberInput,
    GrabberOutput,
    GrabberState,
)


class GrabberStateMachine():
    """State machine for managing control of robot bead grabber"""

    outputs: Dict[GrabberState, GrabberOutput] = {
        GrabberState.REST: {
            'finish': True
        },
        GrabberState.GRAB: {
            'finish': False
        },
        GrabberState.EXTEND_TO_CUP: {
            'finish': False
        },
        GrabberState.RETRACT: {
            'finish': False
        },
        GrabberState.DISPENSE: {
            'finish': False
        }
    }

    def __init__(self, grabber: Grabber) -> None:
        """Initialize starting state and state transition dictionary"""
        self.state: GrabberState = GrabberState.REST
        self.transitions: Dict[GrabberState, Callable[[GrabberInput], None]] = {
            GrabberState.REST: self.transition_from_rest,
            GrabberState.GRAB: self.transition_from_grab,
            GrabberState.EXTEND_TO_CUP: self.transition_from_extend_to_cup,
            GrabberState.RETRACT: self.transition_from_retract,
            GrabberState.DISPENSE: self.transition_from_dispense
        }
        self.grabber = grabber

    def transition(self, input: GrabberInput) -> GrabberOutput:
        """Perform transition and return output of new state"""
        self.transitions[self.state](input)
        return self.outputs[self.state]

    def transition_from_rest(self, input: GrabberInput) -> None:
        """Transition from REST state to next state"""
        tree, cup, net = input['tree'], input['cup'], input['net']
        if tree:
            self.state = GrabberState.GRAB
        elif cup:
            self.state = GrabberState.EXTEND_TO_CUP
        elif net:
            self.state = GrabberState.DISPENSE

    def transition_from_grab(self, input: GrabberInput) -> None:
        """Transition from GRAB state to next state"""
        self.grabber.grab()
        self.state = GrabberState.RETRACT

    def transition_from_extend_to_cup(self, input: GrabberInput) -> None:
        """Transition from EXTEND_TO_CUP state to next state"""
        self.grabber.extend_to_cup()
        self.state = GrabberState.DISPENSE

    def transition_from_retract(self, input: GrabberInput) -> None:
        """Transition from RETRACT state to next state"""
        self.grabber.retract()
        self.state = GrabberState.REST

    def transition_from_dispense(self, input: GrabberInput) -> None:
        """Transition from DISPENSE state to next state"""
        cup = input['cup']
        self.grabber.dispense_beads()
        if cup:
            self.state = GrabberState.RETRACT
        else:
            self.state = GrabberState.REST
