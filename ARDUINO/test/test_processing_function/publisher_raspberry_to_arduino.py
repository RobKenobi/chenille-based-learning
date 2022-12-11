"""
To be run on the raspberry
"""

import serial
from time import sleep

serialArduino = serial.Serial('/dev/ttyUSB0', 115200)

while True:
    # Sending data to the arduino
    # The data are 2 floats separated by ';'
    m = "0.5;0.0\n"
    value = serialArduino.write(m.encode())
    print("Send : ",m)
    sleep(1)
