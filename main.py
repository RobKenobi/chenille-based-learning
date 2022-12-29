import time

import cv2
import serial

from modules.ball_detection import BallDetector
from modules.ball_tracking import BallTracker

# Communication with Arduino
serialArduino = serial.Serial("/dev/ttyUSB0", 115200)

# Ball Detection
detector = BallDetector()

# Parameters for the ball tracker
tolerance = 0.3
height_reference = 0.5
# Ball tracker
tracker = BallTracker(height_reference=height_reference, tolerance=tolerance)

# Video feed
cap = cv2.VideoCapture(0)

# Wait for the camera to be ready
time.sleep(0.1)

last_time = time.time()

while True:
    # Press <ESC>
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break

    # Getting image from camera
    _, image = cap.read()

    if image is not None:
        # Flipping image
        image = cv2.flip(image, -1)

        # Trying to detect the ball
        success, target = detector.detect_ball(image)

        if success:
            x_closet, y_closet, r_closet = target
            cv2.circle(image, (x_closet, y_closet), r_closet, (0, 0, 255), 6)
            cv2.circle(image, (x_closet, y_closet), 2, (0, 255, 255), 3)

            if time.time() - last_time > 0.5:
                deviation = tracker.get_deviation(image, target)
                radius = target[-1]

                target_radius = 70  # The robot should be approximately at 20 cm of the ball

                # TODO : check the reduction factors
                heading_error = deviation[0] / 80
                distance_error = (target_radius - radius) / 20  # (70-10)/20 = 3 rad/s is the maximum longitudinal speed
                servo = 0

                message = f"Distance error : {distance_error}\nHeading error : {heading_error}\nServo : {servo}"
                print(10 * "---")
                print(message)

                message_to_send = f"{distance_error};{heading_error};{servo}"
                serialArduino.write(message_to_send.encode())
                last_time = time.time()

            # TODO : send infos to MQTT server

        cv2.imshow("Image", image)
