from robot.hardware.tof import TOF
import RPi.GPIO as GPIO
import board
import time

tof_pins = (10, 9, 11, 26, 19)
for pin in tof_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
time.sleep(0.2)
for pin in tof_pins:
    GPIO.output(pin, GPIO.HIGH)
time.sleep(0.2)
for pin in tof_pins:
    GPIO.output(pin, GPIO.LOW)


i2c = board.I2C()
GPIO.output(tof_pins[0], GPIO.HIGH)
tof1 = TOF(i2c, 0x30)
GPIO.output(tof_pins[1], GPIO.HIGH)
tof2 = TOF(i2c, 0x31)
GPIO.output(tof_pins[2], GPIO.HIGH)
tof3 = TOF(i2c, 0x32)
GPIO.output(tof_pins[3], GPIO.HIGH)
tof4 = TOF(i2c, 0x33)
GPIO.output(tof_pins[4], GPIO.HIGH)
tof5 = TOF(i2c, 0x34)
while True:
    time.sleep(0.5)
    print('Left: {}'.format(tof1.get_distance()))
    print('Middle: {}'.format(tof2.get_distance()))
    print('Right: {}'.format(tof3.get_distance()))
    print('Bottom: {}'.format(tof4.get_distance()))
    print('Top: {}'.format(tof5.get_distance()))