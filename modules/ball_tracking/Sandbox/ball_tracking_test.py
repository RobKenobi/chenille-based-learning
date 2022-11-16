from modules.ball_tracking.Sandbox.BallTracker import BallTracker
import numpy as np
import cv2

TOP = [350, 20, 20]
BOTTOM = [350, 475, 20]
LEFT = [20, 250, 20]
RIGHT = [500, 250, 20]

TOP_LEFT = [20, 20, 20]
TOP_RIGHT = [500, 20, 20]
BOTTOM_LEFT = [20, 475, 20]
BOTTOM_RIGHT = [500, 475, 20]

CENTER = [350, 250, 20]

pos = [TOP, TOP_LEFT, LEFT, BOTTOM_LEFT, BOTTOM, BOTTOM_RIGHT, RIGHT, TOP_RIGHT, CENTER]

# Ball tracker
tracker = BallTracker(height_reference=0.75)
# Video feed
cap = cv2.VideoCapture(0)

i = 0
while True:
    key = cv2.waitKey(1)
    # Press <ESC> to exit
    if key == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
    # Press <n> to see the next position
    elif key == ord("n"):
        i = (i + 1) % len(pos)
    # Press <p> to see the previous position
    elif key == ord("p"):
        i = (i - 1) % len(pos)
    else:
        pass

    success, image = cap.read()

    if success:
        image = cv2.flip(image, 1)
        tracker.draw_cross(image)

        if key == ord("g"):
            x = np.random.randint(image.shape[1])
            y = np.random.randint(image.shape[0])
            pos.insert(i, [x, y, 20])

        print(tracker.display_position(image, pos[i]))

        cv2.imshow("Visu", image)
