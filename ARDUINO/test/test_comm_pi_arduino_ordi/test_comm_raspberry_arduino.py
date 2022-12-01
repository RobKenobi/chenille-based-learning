import serial
from time import sleep

serialArduino = serial.Serial("/dev/ttyUSB0", 115200)

while True:
    serialArduino.write(b"Hello Malak")
    sleep(1)