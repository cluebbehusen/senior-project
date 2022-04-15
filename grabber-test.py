import pigpio
import RPi.GPIO as GPIO

from robot.hardware.stepper_motor import StepperMotor
from robot.subsystems.grabber import Grabber

GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()

stepper = StepperMotor((17, 18), (27, 22))
grabber = Grabber(pi, 12, 15, 14)
stepper.step_backward(200)
grabber.grab()
stepper.step_forward(300)
grabber.retract()
