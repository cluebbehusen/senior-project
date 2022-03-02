from enum import Enum
from typing import TypedDict


class PWM(Enum):
    HIGH = 12
    MID = 8
    LOW = 4
    OFF = 0


class GPIOOutput(Enum):
    HIGH = 1
    LOW = 0


class BaseState(Enum):
    STOP = 1
    START = 2
    STAIGHT = 3
    START_TURN_AROUND = 4
    TURN_AROUND = 5
    VEER_LEFT = 6
    VEER_RIGHT = 7
    TURN_LEFT = 8
    TURN_RIGHT = 9


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
