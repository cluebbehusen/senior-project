from typing import Callable, Dict

from robot.subsystems.launcher import Launcher
from robot.states.state_types import (
    LauncherInput,
    LauncherOutput,
    LauncherState,
)


class LauncherStateMachine():
    """State machine for managing control of robot bead launcher"""

    outputs: Dict[LauncherState, LauncherOutput] = {
        LauncherState.REST: {
            'finish': True
        },
        LauncherState.LAUNCH: {
            'finish': False
        }
    }

    def __init__(self, launcher: Launcher) -> None:
        """Initialize starting state and state transition dictionary"""
        self.state: LauncherState = LauncherState.REST
        self.transitions: Dict[LauncherState, Callable[[LauncherInput], None]] = {
            LauncherState.REST: self.transition_from_rest,
            LauncherState.LAUNCH: self.transition_from_launch
        }
        self.launcher = launcher

    def transition(self, input: LauncherInput) -> LauncherOutput:
        """Perform transition and return output of new state"""
        self.transitions[self.state](input)
        return self.outputs[self.state]

    def transition_from_rest(self, input: LauncherInput) -> None:
        """Transition from REST state to next state"""
        launch = input['launch']
        if launch:
            self.launcher.run()
            self.state = LauncherState.LAUNCH

    def transition_from_launch(self, input: LauncherInput) -> None:
        """Transition from LAUNCH state to next state"""
        finish = input['launch']
        if finish:
            self.launcher.stop()
            self.state = LauncherState.REST
