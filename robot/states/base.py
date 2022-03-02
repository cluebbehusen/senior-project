from typing import Callable, Dict

from robot.states.state_types import (
    BaseInput,
    BaseOutput,
    BaseState,
    GPIOOutput,
    PWM
)


class BaseStateMachine():
    """State machine for managing movement of robot base"""

    outputs: Dict[BaseState, BaseOutput] = {
        BaseState.STOP: {
            'left_pwm': PWM.OFF,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.OFF,
            'right_dir': GPIOOutput.HIGH,
        },
        BaseState.START: {
            'left_pwm': PWM.HIGH,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.HIGH,
        },
        BaseState.STAIGHT: {
            'left_pwm': PWM.HIGH,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.HIGH,
        },
        BaseState.START_TURN_AROUND: {
            'left_pwm': PWM.HIGH,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.TURN_AROUND: {
            'left_pwm': PWM.HIGH,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.VEER_LEFT: {
            'left_pwm': PWM.LOW,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.HIGH,
        },
        BaseState.TURN_LEFT: {
            'left_pwm': PWM.MID,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.HIGH,
        },
        BaseState.VEER_RIGHT: {
            'left_pwm': PWM.HIGH,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.LOW,
            'right_dir': GPIOOutput.HIGH,
        },
        BaseState.TURN_RIGHT: {
            'left_pwm': PWM.HIGH,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.MID,
            'right_dir': GPIOOutput.LOW,
        },
    }

    def __init__(self):
        """Initialize starting state and state transition dictionary"""
        self.state: BaseState = BaseState.START
        self.transitions: Dict[BaseState, Callable[[BaseInput], None]] = {
            BaseState.STOP: self.transition_from_stop,
            BaseState.START: self.transition_from_start,
            BaseState.STAIGHT: self.transition_from_straight,
            BaseState.START_TURN_AROUND: 3,
            BaseState.TURN_AROUND: self.transition_from_turn_around,
            BaseState.VEER_LEFT: self.transition_from_veer_left,
            BaseState.VEER_RIGHT: self.transition_from_veer_right,
            BaseState.TURN_LEFT: self.transition_from_turn_left,
            BaseState.VEER_RIGHT: self.transition_from_turnright,
        }

    def transition(self, input: BaseInput) -> BaseOutput:
        """Perform transition and return output of new state"""
        self.transitions[self.state](input)
        return self.outputs[self.state]

    def transition_from_stop(self, input: BaseInput) -> None:
        """Transition from STOP state to next state"""
        if input['stop']:
            return
        self.state = BaseState.STAIGHT

    def transition_from_start(self, input: BaseInput) -> None:
        """Transition from START state to next state"""
        left, right = input['left_line'], input['right_line']
        magnitude = right - left
        if magnitude == 0:
            return
        elif magnitude < 0:
            self.state = BaseState.VEER_LEFT
        else:
            self.state = BaseState.VEER_RIGHT

    def transition_from_straight(self, input: BaseInput) -> None:
        """Transition from STRAIGHT state to next state"""
        left, right = input['left_line'], input['right_line']
        magnitude = right - left
        if magnitude == 0:
            return
        elif magnitude < -3:
            self.state = BaseState.TURN_LEFT
        elif magnitude < 0:
            self.state = BaseState.VEER_LEFT
        elif magnitude > 3:
            self.state = BaseState.TURN_RIGHT
        else:
            self.state = BaseState.VEER_RIGHT

    def transition_from_turn_around(self, input: BaseInput) -> None:
        """Transition from TURNAROUND state to next state"""
        pass

    def transition_from_veer_left(self, input: BaseInput) -> None:
        """Transition from VEERLEFT state to next state"""
        pass

    def transition_from_veer_right(self, input: BaseInput) -> None:
        """Transition from VEERRIGHT state to next state"""
        pass

    def transition_from_turn_left(self, input: BaseInput) -> None:
        """Transition from TURNLEFT state to next state"""
        pass

    def transition_from_turnright(self, input: BaseInput) -> None:
        """Transition from TURNRIGHT state to next state"""
        pass
