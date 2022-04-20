from enum import Enum
from typing import TypedDict


class PWM(Enum):
    HIGH = 120
    MID = 110
    LOW = 100
    OFF = 0


class GPIOOutput(Enum):
    HIGH = 1
    LOW = 0


class BaseState(Enum):
    START = 0
    STRAIGHT = 1
    START_TURN_AROUND = 2
    TURN_AROUND = 3
    VEER_LEFT = 4
    VEER_RIGHT = 5
    TURN_LEFT = 6
    TURN_RIGHT = 7
    FINISH = 8


class BaseInput(TypedDict):
    stop: bool
    left_tof: float
    middle_tof: float
    right_tof: float
    left_line: int
    right_line: int


class BaseOutput(TypedDict):
    left_pwm: PWM
    left_dir: GPIOOutput
    right_pwm: PWM
    right_dir: GPIOOutput
    pauseable: bool
    finish: bool


class RobotState(Enum):
    EXPECT_TREE = 0
    ADVANCE_TREE = 1
    READY_GRAB = 2
    GRAB = 3
    EXPECT_CUP_NET = 4
    ADVANCE_CUP = 5
    ADVANCE_NET = 6
    READY_DROP = 7
    DROP = 8
    READY_LAUNCH = 9
    LAUNCH = 10
    IGNORE_CUP_NET = 11
    EXPECT_POLE = 12
    IGNORE_POLE = 13


class RobotInput(TypedDict):
    top_tof: float
    bottom_tof: float
    pauseable: bool


class RobotOutput(TypedDict):
    move_base: bool
