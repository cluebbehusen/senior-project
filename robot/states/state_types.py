from enum import Enum
from typing import TypedDict


class PWM(Enum):
    HIGH = 100
    MID = 90
    LOW = 80
    OFF = 0


class GPIOOutput(Enum):
    HIGH = 1
    LOW = 0


class BaseState(Enum):
    REST = 1
    START = 2
    STRAIGHT = 3
    START_TURN_AROUND = 4
    TURN_AROUND = 5
    VEER_LEFT = 6
    VEER_RIGHT = 7
    TURN_LEFT = 8
    TURN_RIGHT = 9
    FINISH = 10


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


class LiftState(Enum):
    REST = 0
    RAISE = 1
    INCREMENT = 2
    LOWER = 3
    RESET = 4


class LiftInput(TypedDict):
    lift: bool
    increment: bool
    lower: bool
    reset: bool


class LiftOutput(TypedDict):
    finish: bool


class GrabberState(Enum):
    REST = 0
    GRAB = 1
    EXTEND_TO_CUP = 2
    RETRACT = 3
    DISPENSE = 4


class GrabberInput(TypedDict):
    tree: bool
    cup: bool
    net: bool


class GrabberOutput(TypedDict):
    finish: bool


class LauncherState(Enum):
    REST = 0
    LAUNCH = 1


class LauncherInput(TypedDict):
    launch: bool
    finish: bool


class LauncherOutput(TypedDict):
    finish: bool
