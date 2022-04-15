import board
import pigpio
import RPi.GPIO as GPIO
import time
from typing import TypedDict

from robot.hardware.brushed_motor import BrushedMotor
from robot.hardware.line_follow_array import LineFollowArray
from robot.hardware.tof import TOF

from robot.subsystems.grabber import Grabber
from robot.subsystems.launcher import Launcher
from robot.subsystems.lift import Lift

tof_pins = (10, 9, 11, 19, 26)

line_pins = [0, 1, 2, 3, 4, 5, 6, 7]

left_pwm_pin = 16
right_pwm_pin = 13
left_dir_pin = 20
right_dir_pin = 21

coil_pwm_pin = 15
coil_dir_pin = 14
linear_actuator_pwm_pin = 12

launcher_pwm_pin = 22
launcher_dir_pin = 23

phase_a_pins = (0, 0)
phase_b_pins = (0, 0)


class TOFDevices(TypedDict):
    left: TOF
    middle: TOF
    right: TOF
    top: TOF
    bottom: TOF


def init_tof(i2c: board.I2C) -> TOFDevices:
    for pin in tof_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)
    for pin in tof_pins:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.02)
    for pin in tof_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.output(tof_pins[0], GPIO.HIGH)
    left = TOF(i2c, 0x30)
    GPIO.output(tof_pins[1], GPIO.HIGH)
    middle = TOF(i2c, 0x31)
    GPIO.output(tof_pins[2], GPIO.HIGH)
    right = TOF(i2c, 0x32)
    GPIO.output(tof_pins[3], GPIO.HIGH)
    top = TOF(i2c, 0x33)
    GPIO.output(tof_pins[4], GPIO.HIGH)
    bottom = TOF(i2c, 0x34)
    return {
        'left': left,
        'middle': middle,
        'right': right,
        'top': top,
        'bottom': bottom
    }


class Subsystems(TypedDict):
    left_motor: BrushedMotor
    right_motor: BrushedMotor
    line_follower: LineFollowArray
    grabber: Grabber
    launcher: Launcher
    lift: Lift


def init_subsystems(pi: pigpio.pi, i2c: board.I2C) -> Subsystems:
    left_motor = BrushedMotor(pi, left_dir_pin, left_pwm_pin, 10000)
    right_motor = BrushedMotor(pi, right_dir_pin, right_pwm_pin, 10000)
    line_follower = LineFollowArray(i2c, line_pins)
    grabber = Grabber(pi, linear_actuator_pwm_pin, coil_pwm_pin, coil_dir_pin)
    launcher = Launcher(pi, launcher_pwm_pin, launcher_dir_pin)
    lift = Lift(phase_a_pins, phase_b_pins)
    return {
        'left_motor': left_motor,
        'right_motor': right_motor,
        'line_follower': line_follower,
        'grabber': grabber,
        'launcher': launcher,
        'lift': lift
    }


def stop_subsystems(subsystems: Subsystems) -> None:
    left_motor, right_motor = subsystems['left_motor'], subsystems['right_motor']
    left_motor.set_motor_pwm(0)
    right_motor.set_motor_pwm(0)
    subsystems['grabber'].stop()
    subsystems['launcher'].stop()
    subsystems['lift'].stop()
