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
            print(r_closet)
            cv2.circle(image, (x_closet, y_closet), r_closet, (0, 0, 255), 6)
            cv2.circle(image, (x_closet, y_closet), 2, (0, 255, 255), 3)

            if time.time() - last_time > 1:
                deviation = tracker.get_deviation(image, target)
                radius = target[-1]

                target_radius = 70  # The robot should be approximately at 20 cm of the ball

                # TODO : check the reduction factors
                heading_error = deviation[1] / (320 * radius)
                distance_error = (target_radius - radius) / 15
                servo = 0

                message = f"{distance_error};{heading_error};{servo}"
                serialArduino.write(message.encode())
                last_time = time.time()

            # TODO : send infos to MQTT server

    cv2.imshow("Image", image)
