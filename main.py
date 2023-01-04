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
print("Init status : ", status)

def update_population(client, userdata, message):
    global i
    print("update pop ", i)
    i = int(message.payload.decode())


def get_status(client, userdata, message):
    global status
    print("Get status : ", status)
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
# Status :
# -1: waiting for instructions from the server 
# 0: follower 
# 1:leader

print("Status before publish : ", status)
client.publish(f"Chenille-based-learning/Robots/{name_robot}/status", status, qos=2)

"""
    MAIN LOOP
"""
last_command_time = time.time()

try:
    while True:
        #
        k = cv2.waitKey(1)

        # Press <ESC> to exit the program
        if k == 27:
            raise KeyboardInterrupt

        # Reading image from camera
        _, image = cap.read()

        if image is not None:
            # Flipping image
            image = cv2.flip(image, -1)

            """
                Looking for the ball
            """
            # Trying to detect the ball
            success, target = ball_detector.detect_ball(image)

            if not success:
                # Skip all instructions and go back to the beginning of the loop
                continue
            # TODO DEBUG
            print(type(target[-1]), target[-1]) 

            # Publishing the radius of the ball
            client.publish(f"Chenille-based-learning/Robots/{name_robot}/BallRadius", target[-1], qos=1)

            if status == -1:
                # Robot is not allowed to move
                print("Waiting for new status")
                continue

            if time.time() - last_command_time > 0.5:
                # LEADER
                if status == 1:
                    deviation = tracker.get_deviation(image, target)
                    radius = target[-1]

                    target_radius = 70  # The robot should be approximately at 20 cm of the ball

                    heading_error = - deviation[0]
                    distance_error = (target_radius - radius) / 60
                    servo = 0

                # FOLLOWER
                else:
                    # Convert BRG image to GRAY image
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # Trying to detect the ball
                    success, *_ = aruco_detector.detection(gray)

                    if success:
                        heading_error, distance_error = aruco_detector.get_deviation()
                        heading_error /= 25
                        distance_error /= 10
                        servo = 0
                    # If the aruco is not detected
                    else:
                        distance_error = 0
                        heading_error = -0.5  # Turn right
                        servo = 0

                print(10 * "---")
                print(f"Distance error : {distance_error}\nHeading error : {heading_error}\nServo : {servo}")

                message_to_send = f"{distance_error};{heading_error};{servo}\n"
                serialArduino.write(message_to_send.encode())
                last_time = time.time()

            cv2.imshow("Image", image)



except KeyboardInterrupt:
    # Closing communication
    print("Disconnecting from the broker ...")
    client.publish("Chenille-based-learning/Server/population", i - 1, qos=2, retain=True)
    client.disconnect()
    client.loop_stop()

    # Releasing camera
    cap.release()

    # Closing all windows
    cv2.destroyAllWindows()