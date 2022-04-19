import RPi.GPIO as GPIO
import time

from robot.run_course import run_course

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:  # Run forever
    if GPIO.input(4) == GPIO.HIGH:
        run_course()
        time.sleep(3)
        break
