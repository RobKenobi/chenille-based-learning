import time
import argparse

import cv2
import paho.mqtt.client as mqtt
import serial

from modules.aruco import ArucoDetector
from modules.ball_detection import BallDetector
from modules.ball_tracking import BallTracker

"""
    RETRIEVE ROBOT ID
"""

parser = argparse.ArgumentParser(description='Get the robot ID')
parser.add_argument("robot_id", choices=["Robot1", "Robot2"])
# Parse passed arguments
args = parser.parse_args()
# Retrieve robot ID
name_robot = args.robot_id


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
ball_tracker = BallTracker(height_reference=height_reference, tolerance=tolerance)

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


def get_status(client, userdata, message):
    global status
    # print("Get status : ", status)
    status = int(message.payload.decode())


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
        client.subscribe("Chenille-based-learning/Robots/#")
    else:
        print("Connection failed")


broker = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client(name_robot, clean_session=True)

# Callbacks
client.on_connect = on_connect

client.connect(broker, broker_port, keepalive=10)

client.loop_start()  # Start the loop

while not Connected:  # Wait for the client to connect
    time.sleep(1)

status = -1
# Status :
# -1: waiting for instructions from the server 
# 0: follower 
# 1:leader

client.publish(f"Chenille-based-learning/Robots/{name_robot}/status", status, qos=2)
client.message_callback_add(f"Chenille-based-learning/Robots/{name_robot}/status", get_status)

"""
    MAIN LOOP
"""

last_command_time = time.time()

try:
    while True:
        # Press <ESC> to exit the program
        if cv2.waitKey(1) == 27:
            raise KeyboardInterrupt

        # Reading image from camera
        image_received, image = cap.read()

        if image_received:
            # Flipping image
            image = cv2.flip(image, -1)

            """
                Looking for the ball
            """
            # Trying to detect the ball
            success_ball, target = ball_detector.detect_ball(image)

            if not success_ball:
                print("I don't see the ball")
                target = [0, 0, 0]
                heading_error = 0
                distance_error = 0
            else:
                print("\nI see the ball\n")

            # Publishing the radius of the ball
            client.publish(f"Chenille-based-learning/Robots/{name_robot}/BallRadius", int(target[-1]), qos=1)

            if status == -1:
                # Robot is not allowed to move
                print("Waiting for new status")
                cv2.imshow("Image", image)
                time.sleep(0.5)
                continue

            if time.time() - last_command_time > 0.5:
                # LEADER
                if status == 1 and success_ball:
                    # Retrieving deviation and radius
                    deviation = ball_tracker.get_deviation(image, target)
                    radius = target[-1]

                    target_radius = 70  # The robot should be approximately at 20 cm of the ball

                    # Computing error with reduction factors
                    heading_error = - deviation[0] / 175
                    distance_error = (target_radius - radius) / 70

                # FOLLOWER
                else:
                    # Convert BRG image to GRAY image
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # Trying to detect the aruco
                    success, *_ = aruco_detector.detection(gray)

                    if success:
                        print("I see the aruco")

                        # Retrieving error with reduction factors
                        heading_error, distance_error = aruco_detector.get_deviation()
                        heading_error /= 25
                        distance_error /= 10

                    # If the aruco is not detected
                    else:
                        print("I don't see the aruco")
                        distance_error = 0
                        heading_error = -0.5  # Turn right

                print(10 * "---")
                print(f"Distance error : {round(distance_error, 2)}\nHeading error  : {round(heading_error, 2)}\n")

                message_to_send = f"{round(distance_error, 2)};{round(heading_error, 2)}\n"
                serialArduino.write(message_to_send.encode())
                last_time = time.time()

            cv2.imshow("Image", image)

except KeyboardInterrupt:
    # Closing communication
    print("Disconnecting from the broker ...")
    client.publish(f"Chenille-based-learning/Robots/{name_robot}/BallRadius", 0, qos=1)
    client.disconnect()
    client.loop_stop()

    # Releasing camera
    cap.release()

    # Closing all windows
    cv2.destroyAllWindows()
