from robot.hardware.brushed_motor import BrushedMotor
import pigpio
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pi = pigpio.pi()
motor = BrushedMotor(pi, 14, 15, 10000)
motor.set_direction_forward()
motor.set_motor_pwm(100)
time.sleep(1)
motor.set_motor_pwm(0)
