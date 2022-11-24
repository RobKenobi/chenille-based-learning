import sys
import os
MODULES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, MODULES_DIR)

from modules.ball_detection import BallDetector, FilterColorEditor, CircleDetectorEditor
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
            x_closet, y_closet, r_closet = target
            cv2.circle(image, (x_closet, y_closet), r_closet, (0, 0, 255), 6)
            cv2.circle(image, (x_closet, y_closet), 2, (0, 255, 255), 3)

        cv2.imshow("Visu", image)
