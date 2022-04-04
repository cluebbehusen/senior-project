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
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.START: {
            'left_pwm': PWM.HIGH_LEFT,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.STRAIGHT: {
            'left_pwm': PWM.HIGH_LEFT,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.START_TURN_AROUND: {
            'left_pwm': PWM.HIGH_LEFT,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.TURN_AROUND: {
            'left_pwm': PWM.HIGH_LEFT,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.VEER_LEFT: {
            'left_pwm': PWM.LOW,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.TURN_LEFT: {
            'left_pwm': PWM.HIGH_LEFT,
            'left_dir': GPIOOutput.HIGH,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.VEER_RIGHT: {
            'left_pwm': PWM.HIGH_LEFT,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.LOW,
            'right_dir': GPIOOutput.LOW,
        },
        BaseState.TURN_RIGHT: {
            'left_pwm': PWM.HIGH_LEFT,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.HIGH,
            'right_dir': GPIOOutput.HIGH,
        },
        BaseState.FINISH: {
            'left_pwm': PWM.OFF,
            'left_dir': GPIOOutput.LOW,
            'right_pwm': PWM.OFF,
            'right_dir': GPIOOutput.LOW,
        }
    }

    def __init__(self):
        """Initialize starting state and state transition dictionary"""
        self.state: BaseState = BaseState.START
        self.transitions: Dict[BaseState, Callable[[BaseInput], None]] = {
            BaseState.STOP: self.transition_from_stop,
            BaseState.START: self.transition_from_start,
            BaseState.STRAIGHT: self.transition_from_straight,
            BaseState.START_TURN_AROUND: self.transition_from_start_turn_around,
            BaseState.TURN_AROUND: self.transition_from_turn_around,
            BaseState.VEER_LEFT: self.transition_from_veer_left,
            BaseState.VEER_RIGHT: self.transition_from_veer_right,
            BaseState.TURN_LEFT: self.transition_from_turn_left,
            BaseState.TURN_RIGHT: self.transition_from_turn_right,
            BaseState.FINISH: self.transition_from_finish,
        }

    def transition(self, input: BaseInput) -> BaseOutput:
        """Perform transition and return output of new state"""
        self.transitions[self.state](input)
        return self.outputs[self.state]

    def transition_from_stop(self, input: BaseInput) -> None:
        """Transition from STOP state to next state"""
        return

    def transition_from_start(self, input: BaseInput) -> None:
        """Transition from START state to next state"""
        left, right = input['left_line'], input['right_line']
        middle_tof = input['middle_tof']
        magnitude = right - left
        if magnitude < 0 and middle_tof < 35:
            self.state = BaseState.VEER_LEFT
        elif magnitude > 0 and middle_tof < 35:
            self.state = BaseState.VEER_RIGHT

    def transition_from_straight(self, input: BaseInput) -> None:
        """Transition from STRAIGHT state to next state"""
        left, right = input['left_line'], input['right_line']
        magnitude = right - left
        left_tof, middle_tof, right_tof = (
            input['left_tof'], input['middle_tof'], input['right_tof'])
        boxed_in = left_tof < 15 and right_tof < 15
        if boxed_in and middle_tof < 5 and left == 10 and right == 10:
            self.state = BaseState.FINISH
        elif boxed_in and middle_tof < 10 and left != 10 and right != 10:
            self.state = BaseState.START_TURN_AROUND
        elif magnitude < 0:
            self.state = BaseState.TURN_LEFT
        elif magnitude > 0:
            self.state = BaseState.TURN_RIGHT

    def transition_from_start_turn_around(self, input: BaseInput) -> None:
        """Transition from START_TURN_AROUND state to next state"""
        left, right = input['left_line'], input['right_line']
        if left <= 3 and right <= 0:
            self.state = BaseState.TURN_AROUND

    def transition_from_turn_around(self, input: BaseInput) -> None:
        """Transition from TURN_AROUND state to next state"""
        left, right = input['left_line'], input['right_line']
        if left != 0 and right != 0:
            self.state = BaseState.STRAIGHT
        elif right > 7:
            self.state = BaseState.TURN_RIGHT
        elif left > 7:
            self.state = BaseState.TURN_LEFT

    def transition_from_veer_left(self, input: BaseInput) -> None:
        """Transition from VEER_LEFT state to next state"""
        left, right = input['left_line'], input['right_line']
        middle_tof = input['middle_tof']
        magnitude = right - left
        if left <= 1 or magnitude > 0 or middle_tof < 10:
            self.state = BaseState.STRAIGHT
        elif left > 3:
            self.state = BaseState.TURN_LEFT

    def transition_from_veer_right(self, input: BaseInput) -> None:
        """Transition from VEER_RIGHT state to next state"""
        left, right = input['left_line'], input['right_line']
        middle_tof = input['middle_tof']
        magnitude = right - left
        if right <= 1 or magnitude < 0 or middle_tof < 10:
            self.state = BaseState.STRAIGHT
        elif right > 3:
            self.state = BaseState.TURN_RIGHT

    def transition_from_turn_left(self, input: BaseInput) -> None:
        """Transition from TURN_LEFT state to next state"""
        left, right = input['left_line'], input['right_line']
        magnitude = abs(right - left)
        if magnitude < 1:
            self.state = BaseState.STRAIGHT
        elif left <= 3:
            self.state = BaseState.VEER_LEFT

    def transition_from_turn_right(self, input: BaseInput) -> None:
        """Transition from TURN_RIGHT state to next state"""
        left, right = input['left_line'], input['right_line']
        magnitude = abs(right - left)
        if magnitude < 1:
            self.state = BaseState.STRAIGHT
        elif right <= 3:
            self.state = BaseState.VEER_RIGHT

    def transition_from_finish(self, input: BaseInput) -> None:
        """Transition from FINISH state to next state"""
        return