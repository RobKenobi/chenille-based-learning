import time

import cv2
import paho.mqtt.client as mqtt
import serial

from modules.aruco import ArucoDetector
from modules.ball_detection import BallDetector
from modules.ball_tracking import BallTracker

"""
    ARDUINO - RASPBERRY COMMUNICATION
"""

# Communication with Arduino
serialArduino = serial.Serial("/dev/ttyUSB0", 115200)

"""
    TARGET DETECTION
"""

# Aruco Detection
aruco_detector = ArucoDetector()

# Ball Detection
ball_detector = BallDetector()

# Parameters for the ball tracker
tolerance = 0.05
height_reference = 0.5

# Ball tracker
tracker = BallTracker(height_reference=height_reference, tolerance=tolerance)

"""
    CAMERA INITIALIZATION
"""

# Video feed
cap = cv2.VideoCapture(0)

# Wait for the camera to be ready
time.sleep(0.1)

"""
    COMMUNICATION
"""

Connected = False

i = None

status = -1


def update_population(client, userdata, message):
    global i
    print("update pop ", i)
    i = int(message.payload.decode())


def get_status(client, userdata, message):
    global status
    status = int(message.payload.decode())


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
        client.subscribe("Chenille-based-learning/Server/population")
        client.subscribe("Chenille-based-learning/Robots/#")
    else:
        print("Connection failed")


broker = "broker.hivemq.com"
broker_port = 1883

name_robot = "Robot1"
client = mqtt.Client(name_robot, clean_session=True)

# Callbacks
client.on_connect = on_connect

client.message_callback_add("Chenille-based-learning/Server/population", update_population)
client.message_callback_add(f"Chenille-based-learning/Robots/{name_robot}/status", get_status)

client.connect(broker, broker_port, keepalive=10)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    time.sleep(1)

client.publish("Chenille-based-learning/Server/population", i + 1, qos=2, retain=True)
# -1: waiting for instructions from the server 0: follower 1:leader

client.publish(f"Chenille-based-learning/Robots/{name_robot}/status", status, qos=1)

"""
    MAIN LOOP
"""
last_command_time = time.time()

try:
    while True:
        #
        _, image = cap.read()

        # TODO  LOOK FOR BLUE BALL

except KeyboardInterrupt:
    print("Disconnecting from the broker ...")
    client.publish("Chenille-based-learning/Server/population", i - 1, qos=2, retain=True)
    client.disconnect()
    client.loop_stop()
