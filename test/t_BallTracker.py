import sys
import os
MODULES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, MODULES_DIR)

from modules.ball_detection import BallDetector, FilterColorEditor, CircleDetectorEditor
from modules.ball_tracking import BallTracker
import cv2

# Color Detection
filter = FilterColorEditor()
color_params = filter.open_editor()

# Circle Detection
circle_detector = CircleDetectorEditor(mask_params=color_params)
circle_params = circle_detector.open_editor()

# Ball Detection
detector = BallDetector(color_filter_params=color_params, circle_detector_params=circle_params)

print("\n < BALL DETECTOR > \n")

# Parameters for the ball tracker
tolerance = 0.3
height_reference = 0.5
# Ball tracker
tracker = BallTracker(height_reference=height_reference, tolerance=tolerance)

print("\n < BALL TRACKER > \n")
print("Press <ESC> to exit")

cap = cv2.VideoCapture(0)
while True:
    # If <ESC> is pressed
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break

    # Getting image
    success, image = cap.read()

    if success:
        # Flipping image
        image = cv2.flip(image, 1)

        # Trying to detect the ball
        success, target = detector.detect_ball(image)

        if success:
            print(tracker.display_position(image, target))

        cv2.imshow("Visu", image)
