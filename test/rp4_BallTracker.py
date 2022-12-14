import os
import sys

MODULES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, MODULES_DIR)

from modules.ball_detection import BallDetector
from modules.ball_tracking import BallTracker

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Ball Detection
detector = BallDetector()

print("\n < BALL DETECTOR > \n")

# Parameters for the ball tracker
tolerance = 0.3
height_reference = 0.5
# Ball tracker
tracker = BallTracker(height_reference=height_reference, tolerance=tolerance)

# Initialize the Pi camera
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# Wait for the camera to be ready
time.sleep(0.1)

# cap = cv2.VideoCapture(0)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = rawCapture.array
    cv2.imwrite("raw_image.png", image)
    # If <ESC> is pressed
    if cv2.waitKey(1) == 27:
        camera.close()
        break

    if image is not None:  # if an image is detected
        # Flipping image
        image = cv2.flip(image, -1)
        cv2.imwrite("test_image.png", image)
        # Trying to detect the ball
        success, target = detector.detect_ball(image)
        print(success)
        if success:
            deviation = tracker.get_deviation(image, target)
            print("Deviation : ", deviation)

    rawCapture.truncate()
    rawCapture.seek(0)
    # cv2.imshow("Visu", image)
