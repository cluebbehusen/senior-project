import board
import time
from robot.drivers.sx1509 import SX1509


def print_ir_values(line_ir, line_ir_pins):
    ir_values = []
    for pin in line_ir_pins:
        ir_values.append(line_ir.digitalRead(pin))
    print(ir_values)


# Set up i2c
comm_port = board.I2C()

line_ir_pins = [0, 1, 2, 3, 4, 5, 6, 7]

# Initialize the expander
line_ir = SX1509(comm_port)
line_ir.clock(oscDivider=4)

# Set up pins in expander
for pin in line_ir_pins:
    line_ir.pinMode(pin, 0)

while True:
    print_ir_values(line_ir, line_ir_pins)
    time.sleep(0.5)