import board
import RPi.GPIO as GPIO
import time

from robot.hardware.line_follow_array import LineFollowArray
from robot.hardware.tof import TOF
from robot.states.base import BaseStateMachine
from robot.states.state_types import BaseInput

if __name__ == '__main__':
    i2c = board.I2C()

    left_pwm_pin = 18
    right_pwm_pin = 13
    left_dir_pin = 23
    right_dir_pin = 24

    GPIO.setup(left_dir_pin, GPIO.OUT)
    GPIO.setup(right_dir_pin, GPIO.OUT)
    GPIO.output(left_dir_pin, GPIO.LOW)
    GPIO.output(right_dir_pin, GPIO.LOW)

    GPIO.setup(left_pwm_pin, GPIO.OUT)
    GPIO.setup(right_pwm_pin, GPIO.OUT)
    left_pwm = GPIO.PWM(left_pwm_pin, 10000)
    right_pwm = GPIO.PWM(right_pwm_pin, 10000)
    left_pwm.start(0)
    right_pwm.start(0)

    tof_pins = (17, 27, 22)
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

    line_pins = [0, 1, 2, 3, 4, 5, 6, 7]
    line_follower = LineFollowArray(i2c, line_pins)

    base_state_machine = BaseStateMachine()
    count = 0

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
        if old_state != new_state or count > 30:
            if old_state != new_state:
                print('=== State Change Occurred ===')
                print('{} -> {}'.format(old_state, new_state))
            print('{}: {}'.format(base_state_machine.state, input))
            count = 0
        left_pwm.ChangeDutyCycle(output['left_pwm'].value)
        right_pwm.ChangeDutyCycle(output['right_pwm'].value)
        GPIO.output(left_dir_pin, output['left_dir'].value)
        GPIO.output(right_dir_pin, output['right_dir'].value)
        time.sleep(1 / 30)
        count += 1
