import serial
import random
from time import sleep

serialArduino = serial.Serial("/dev/ttyUSB0",9600)

i = 0
while True:
    print(i)
    message = str(i)+"\n"
    serialArduino.write(message.encode())
    i += 1
    sleep(1)
