import RPi.GPIO as GPIO
from robot.subsystems.lift import Lift

GPIO.setmode(GPIO.BCM)

phase_a_pins = (17, 18)
phase_b_pins = (27, 22)

lift = Lift(phase_a_pins, phase_b_pins)
lift.reset()
