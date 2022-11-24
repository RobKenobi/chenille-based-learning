import sys
import os
MODULES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, MODULES_DIR)

from modules.ball_detection import BallDetector, FilterColorEditor, CircleDetectorEditor
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

#cap = cv2.VideoCapture(0)
while True:
    # If <ESC> is pressed
    if cv2.waitKey(1) == 27:
        break

    # Getting image
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    print(image)
    if image:
        # Flipping image
        image = cv2.flip(image, 1)

        # Trying to detect the ball
        success, target = detector.detect_ball(image)

        if success:
            print(tracker.display_position(image, target))

        # cv2.imshow("Visu", image)