from robot.hardware.line_follow_array import LineFollowArray
import board

i2c = board.I2C()
pins_array = [0, 1, 2, 3, 4, 5, 6, 7]
array = LineFollowArray(i2c, pins_array)
print(array.get_sensor_reading_magnitudes())
