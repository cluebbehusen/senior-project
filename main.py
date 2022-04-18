from multiprocessing.managers import RemoteError
import board
import time
import pigpio

from robot.states.base import BaseStateMachine
from robot.states.robot import RobotStateMachine
from robot.states.state_types import BaseInput, RobotInput
from robot.utils.init import init_tof, init_subsystems, stop_subsystems
from robot.utils.play_song import play_song, stop_song


def run_course():
    i2c = board.I2C()
    pi = pigpio.pi()

    tof_devices = init_tof(i2c)
    subsystems = init_subsystems(pi, i2c)
    line_follower = subsystems['line_follower']
    left_motor, right_motor = subsystems['left_motor'], subsystems['right_motor']

    base_state_machine = BaseStateMachine()
    robot_state_machine = RobotStateMachine(
        subsystems['grabber'],
        subsystems['launcher'],
        subsystems['lift'])

    media_player = play_song('dancing.mp4')

    try:
        while True:
            try:
                left_tof = tof_devices['left'].get_distance()
                middle_tof = tof_devices['middle'].get_distance()
                right_tof = tof_devices['right'].get_distance()
                top_tof = tof_devices['top'].get_distance()
                bottom_tof = tof_devices['bottom'].get_distance()
            except BaseException:
                print('[!] ToF error occurred, resetting sensors')
                left_motor.set_motor_pwm(0)
                right_motor.set_motor_pwm(0)
                tof_devices = init_tof(i2c)
                continue
            try:
                line = line_follower.get_sensor_reading_magnitudes()
                left_line, right_line = line
            except BaseException:
                print('[!] Line follower array error occurred')
                left_motor.set_motor_pwm(0)
                right_motor.set_motor_pwm(0)
                continue
            base_input: BaseInput = {
                'stop': False,
                'left_tof': left_tof,
                'middle_tof': middle_tof,
                'right_tof': right_tof,
                'left_line': left_line,
                'right_line': right_line,
            }
            old_base_state = base_state_machine.state
            base_output = base_state_machine.transition(base_input)
            new_base_state = base_state_machine.state
            pauseable = base_output['pauseable']
            robot_input: RobotInput = {
                'top_tof': top_tof,
                'bottom_tof': bottom_tof,
                'pauseable': pauseable,
            }
            old_robot_state = robot_state_machine.state
            robot_output = robot_state_machine.transition(robot_input)
            new_robot_state = robot_state_machine.state
            move_base = robot_output['move_base']
            if not move_base:
                left_motor.set_motor_pwm(0)
                right_motor.set_motor_pwm(0)
            else:
                left_motor.set_motor_pwm(base_output['left_pwm'].value)
                right_motor.set_motor_pwm(base_output['right_pwm'].value)
                left_motor.set_direction(base_output['left_dir'].value)
                right_motor.set_direction(base_output['right_dir'].value)
            if old_base_state != new_base_state:
                print('=== State Change Occurred ===')
                print('{} -> {}'.format(old_base_state, new_base_state))
            print('BASE: {}: {}'.format(base_state_machine.state, base_input))
            if old_robot_state != new_robot_state:
                print('=== State Change Occurred ===')
                print('{} -> {}'.format(old_robot_state, new_robot_state))
            print(
                'ROBOT: {}: {}'.format(
                    robot_state_machine.state,
                    robot_input))
            print('CUP/NET COUNT: {}'.format(robot_state_machine.cup_net_count))
            finish = base_output['finish']
            if finish:
                break
            time.sleep(1 / 60)
    except BaseException as e:
        print(e)
        stop_song(media_player)
        stop_subsystems(subsystems)
    stop_song(media_player)
    stop_subsystems(subsystems)


if __name__ == '__main__':
    run_course()
