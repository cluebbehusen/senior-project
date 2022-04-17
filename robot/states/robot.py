from typing import Callable, Dict

from robot.states.state_types import (
    RobotInput,
    RobotOutput,
    RobotState
)
from robot.subsystems.grabber import Grabber
from robot.subsystems.launcher import Launcher
from robot.subsystems.lift import Lift


class RobotStateMachine():
    """State machine for managing robot's beads subsystems"""

    detection_threshold: float = 15.5
    rejection_threshold: float = 21.0

    outputs: Dict[RobotState, RobotOutput] = {
        RobotState.EXPECT_TREE: {
            'move_base': True,
        },
        RobotState.ADVANCE_TREE: {
            'move_base': True,
        },
        RobotState.READY_GRAB: {
            'move_base': False,
        },
        RobotState.GRAB: {
            'move_base': False,
        },
        RobotState.EXPECT_CUP_NET: {
            'move_base': True,
        },
        RobotState.ADVANCE_CUP: {
            'move_base': True,
        },
        RobotState.ADVANCE_NET: {
            'move_base': True,
        },
        RobotState.READY_DROP: {
            'move_base': False,
        },
        RobotState.DROP: {
            'move_base': False,
        },
        RobotState.READY_LAUNCH: {
            'move_base': False,
        },
        RobotState.LAUNCH: {
            'move_base': False,
        },
        RobotState.IGNORE_CUP_NET: {
            'move_base': True,
        },
        RobotState.EXPECT_POLE: {
            'move_base': True,
        },
        RobotState.IGNORE_POLE: {
            'move_base': True
        }
    }

    def __init__(
            self,
            grabber: Grabber,
            launcher: Launcher,
            lift: Lift):
        """Initialize starting state, state transition dictionary, and subsystems"""
        self.cup_net_count: int = 0
        self.advance_count: int = 0
        self.grabber: Grabber = grabber
        self.launcher: Launcher = launcher
        self.lift: Lift = lift
        self.state: RobotState = RobotState.EXPECT_TREE
        self.transitions: Dict[RobotState, Callable[[RobotInput], None]] = {
            RobotState.EXPECT_TREE: self.transition_from_expect_tree,
            RobotState.ADVANCE_TREE: self.transition_from_advance_tree,
            RobotState.READY_GRAB: self.transition_from_ready_grab,
            RobotState.GRAB: self.transition_from_grab,
            RobotState.EXPECT_CUP_NET: self.transition_from_expect_cup_net,
            RobotState.ADVANCE_CUP: self.transition_from_advance_cup,
            RobotState.ADVANCE_NET: self.transition_from_advance_net,
            RobotState.READY_DROP: self.transition_from_ready_drop,
            RobotState.DROP: self.transition_from_drop,
            RobotState.READY_LAUNCH: self.transition_from_ready_launch,
            RobotState.LAUNCH: self.transition_from_launch,
            RobotState.IGNORE_CUP_NET: self.transition_from_ignore_cup_net,
            RobotState.EXPECT_POLE: self.transition_from_expect_pole,
            RobotState.IGNORE_POLE: self.transition_from_ignore_pole,
        }

    def transition(self, input: RobotInput) -> RobotOutput:
        """Perform transition and return output of new state"""
        self.transitions[self.state](input)
        return self.outputs[self.state]

    def transition_from_expect_tree(self, input: RobotInput) -> None:
        """Transition from EXPECT_TREE state to next state"""
        pass

    def transition_from_advance_tree(self, input: RobotInput) -> None:
        """Transition from ADVANCE_TREE state to next state"""
        pass

    def transition_from_ready_grab(self, input: RobotInput) -> None:
        """Transition from READY_GRAB state to next state"""

    def transition_from_grab(self, input: RobotInput) -> None:
        """Transition from GRAB state to next state"""
        pass

    def transition_from_expect_cup_net(self, input: RobotInput) -> None:
        """Transition from EXPECT_CUP_NET state to next state"""
        pass

    def transition_from_advance_cup(self, input: RobotInput) -> None:
        """Transition from ADVANCE_CUP state to next state"""
        pass

    def transition_from_advance_net(self, input: RobotInput) -> None:
        """Transition from ADVANCE_CUP state to next state"""
        pass

    def transition_from_ready_drop(self, input: RobotInput) -> None:
        """Transition from READY_DROP state to next state"""
        pass

    def transition_from_drop(self, input: RobotInput) -> None:
        """Transition from DROP state to next state"""
        pass

    def transition_from_ready_launch(self, input: RobotInput) -> None:
        """Transition from READY_LAUNCH state to next state"""
        pass

    def transition_from_launch(self, input: RobotInput) -> None:
        """Transition from LAUNCH state to next state"""
        pass

    def transition_from_ignore_cup_net(self, input: RobotInput) -> None:
        """Transition from IGNORE_CUP_NET state to next state"""
        pass

    def transition_from_expect_pole(self, input: RobotInput) -> None:
        """Transition from EXPECT_POLE state to next state"""
        pass

    def transition_from_ignore_pole(self, input: RobotInput) -> None:
        """Transition from IGNORE_POLE state to next state"""
        pass
