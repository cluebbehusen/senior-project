from robot.hardware.stepper_motor import StepperMotor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
motor = StepperMotor((17, 18), (27, 22))
motor.step_backward(3000)
