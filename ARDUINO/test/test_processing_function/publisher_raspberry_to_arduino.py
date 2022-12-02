"""
To be run on the raspberry
"""

import serial
from time import sleep

serialArduino = serial.Serial('/dev/ttyUSB0', 115200)

while True:
    # Sending data to the arduino
    # The data are 2 floats separated by ';'
    value = serialArduino.write(b"0.9;12.3\n")
    sleep(1)
