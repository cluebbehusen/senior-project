import board
import RPi.GPIO as GPIO
import time
import pigpio

from robot.hardware.line_follow_array import LineFollowArray
from robot.hardware.tof import TOF
from robot.hardware.brushed_motor import BrushedMotor
from robot.states.base import BaseStateMachine
from robot.states.state_types import BaseInput

if __name__ == '__main__':
    i2c = board.I2C()
    pi = pigpio.pi()

    left_pwm_pin = 16
    right_pwm_pin = 13
    left_dir_pin = 20
    right_dir_pin = 21

    left_motor = BrushedMotor(pi, left_dir_pin, left_pwm_pin, 10000)
    right_motor = BrushedMotor(pi, right_dir_pin, right_pwm_pin, 10000)

    tof_pins = (10, 9, 11, 19, 26)
    for pin in tof_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    time.sleep(0.2)
    for pin in tof_pins:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.2)
    for pin in tof_pins:
        GPIO.output(pin, GPIO.LOW)

    devices = {}
    GPIO.output(tof_pins[0], GPIO.HIGH)
    devices['left'] = TOF(i2c, 0x30)
    GPIO.output(tof_pins[1], GPIO.HIGH)
    devices['middle'] = TOF(i2c, 0x31)
    GPIO.output(tof_pins[2], GPIO.HIGH)
    devices['right'] = TOF(i2c, 0x32)
    GPIO.output(tof_pins[3], GPIO.HIGH)
    bottom = TOF(i2c, 0x33)
    GPIO.output(tof_pins[4], GPIO.HIGH)
    top = TOF(i2c, 0x34)

    line_pins = [0, 1, 2, 3, 4, 5, 6, 7]
    line_follower = LineFollowArray(i2c, line_pins)

    base_state_machine = BaseStateMachine()
    count = 0

    try:
        while True:
            left_tof = devices['left'].get_distance()
            middle_tof = devices['middle'].get_distance()
            right_tof = devices['right'].get_distance()
            left_line, right_line = line_follower.get_sensor_reading_magnitudes()
            input: BaseInput = {
                'stop': False,
                'left_tof': left_tof,
                'middle_tof': middle_tof,
                'right_tof': right_tof,
                'left_line': left_line,
                'right_line': right_line,
            }
            old_state = base_state_machine.state
            output = base_state_machine.transition(input)
            new_state = base_state_machine.state
            if old_state != new_state or count > 5:
                if old_state != new_state:
                    print('=== State Change Occurred ===')
                    print('{} -> {}'.format(old_state, new_state))
                print('{}: {}'.format(base_state_machine.state, input))
                print(
                    'TOP: {}, BOTTOM: {}'.format(
                        top.get_distance(),
                        bottom.get_distance()))
                count = 0
            left_motor.set_motor_pwm(output['left_pwm'].value)
            right_motor.set_motor_pwm(output['right_pwm'].value)
            left_motor.set_direction(output['left_dir'].value)
            right_motor.set_direction(output['right_dir'].value)
            time.sleep(1 / 60)
            count += 1
    except BaseException as e:
        print(e)
        left_motor.stop_motor()
        right_motor.stop_motor()
