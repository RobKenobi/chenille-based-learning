import serial
import time

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

while True:
    value = arduino.write(b"0.9;12.3")
    time.sleep(0.05)
    print(value)