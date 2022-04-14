from robot.hardware.linear_actuator import LinearActuator
import pigpio

pi = pigpio.pi()
actuator = LinearActuator(pi, 12, 1000)
actuator.set_extension_minimum()
