import board
import time
import pigpio
import RPi.GPIO as GPIO

from robot.states.base import BaseStateMachine
from robot.states.state_types import BaseOutput, PWM, BaseInput, GPIOOutput
from robot.utils.init import init_tof, init_subsystems, stop_subsystems

object_threshold = 18

if __name__ == '__main__':
    i2c = board.I2C()
    pi = pigpio.pi()

    devices = init_tof(i2c)
    subsystems = init_subsystems(pi, i2c)
    line_follower = subsystems['line_follower']
    left_motor, right_motor = subsystems['left_motor'], subsystems['right_motor']

    base_state_machine = BaseStateMachine()
    object_count = 0
    count = 0
    output: BaseOutput = {
        'left_pwm': PWM.OFF,
        'left_dir': GPIOOutput.HIGH,
        'right_pwm': PWM.OFF,
        'right_dir': GPIOOutput.HIGH,
        'pauseable': False
    }

    try:
        while True:
            try:
                left_tof = devices['left'].get_distance()
                middle_tof = devices['middle'].get_distance()
                right_tof = devices['right'].get_distance()
                top_tof = devices['top'].get_distance()
                bottom_tof = devices['bottom'].get_distance()
            except BaseException:
                print('error occurred, resetting sensors')
                left_motor.set_motor_pwm(0)
                right_motor.set_motor_pwm(0)
                devices = init_tof(i2c)
            try:
                left_line, right_line = line_follower.get_sensor_reading_magnitudes()
            except BaseException:
                print('line following sensor error occurred, resetting')
            input: BaseInput = {
                'stop': False,
                'left_tof': left_tof,
                'middle_tof': middle_tof,
                'right_tof': right_tof,
                'left_line': left_line,
                'right_line': right_line,
            }
            old_state = base_state_machine.state
            old_pauseable = output['pauseable']
            output = base_state_machine.transition(input)
            pauseable = output['pauseable']
            if old_pauseable != pauseable:
                object_count = 0
            new_state = base_state_machine.state
            print('OBJECT COUNT: {}'.format(object_count))
            if bottom_tof < object_threshold and pauseable:
                object_count += 1
            if object_count > 20:
                print('DETECTED OBJECT')
                left_motor.set_motor_pwm(0)
                right_motor.set_motor_pwm(0)
                time.sleep(1)
                base_state_machine.state = new_state
                object_count = 0
            if old_state != new_state or count > 3:
                if old_state != new_state:
                    print('=== State Change Occurred ===')
                    print('{} -> {}'.format(old_state, new_state))
                print('{}: {}'.format(base_state_machine.state, input))
                print('TOP: {}, BOTTOM: {}'.format(top_tof, bottom_tof))
                count = 0
                pass
            left_motor.set_motor_pwm(output['left_pwm'].value)
            right_motor.set_motor_pwm(output['right_pwm'].value)
            left_motor.set_direction(output['left_dir'].value)
            right_motor.set_direction(output['right_dir'].value)
            time.sleep(1 / 60)
            count += 1
    except BaseException as e:
        print(e)
        stop_subsystems(subsystems)
