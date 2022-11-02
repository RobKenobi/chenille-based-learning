import cv2
import cv2.cv2
import numpy as np


def empty(x):
    pass


def find_mask():
    # Initializing the webcam

    wCam, hCam = 2340, 1920  # Parameters from camera

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    print('Camera SETUP: OK')

    # Create a window named TrackBars
    # Since we will be using the HSV (Hue,Saturation,Value) format to extract a mask from our image
    # We will create 6 TrackBars to find the best solution depending of what we want to study

    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars", 37, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 133, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 137, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 26, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

    print("Press 'e' to stop the execution")

    while True:
        # Read the camera flow
        success, img = cap.read()

        # Convert the image to HSV format
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Get the position of the tracker
        hue_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        hue_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        sat_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        sat_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        val_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        val_max = cv2.getTrackbarPos("Val Max", "TrackBars")

        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])

        # Create the mask from the image (Perform basic thresholding operations)
        mask = cv2.inRange(img_hsv, lower, upper)

        # Plot the resulting mask
        cv2.imshow("Image", img)
        cv2.imshow("HSV", mask)

        if cv2.waitKey(1) == ord('e'):  # Press e to exit loop
            break

    return lower, upper, mask


def apply_mask(img, lower, upper):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, lower, upper)
    return mask


def find_blue_ball(print_all=False):
    # Initializing the webcam

    wCam, hCam = 2340, 1920  # Parameters from camera

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    print('Camera SETUP: OK')

    # Create a window named TrackBars
    # Since we will be using the HSV (Hue,Saturation,Value) format to extract a mask from our image
    # We will create 6 TrackBars to find the best solution depending of what we want to study
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 290)
    cv2.createTrackbar("Hue Min", "TrackBars", 103, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 170, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 103, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 77, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("Sensitivity: Circles detection", "TrackBars", 100, 300, empty)
    cv2.createTrackbar("Accuracy: Circles detection", "TrackBars", 15, 25, empty)

    prev_circle = None
    while True:
        # Read the camera flow
        success, img = cap.read()

        img_copy = img.copy()
        """ 
        Finding the blue color
        """
        # Convert the image to HSV format
        img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

        # Get the position of the tracker
        hue_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        hue_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        sat_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        sat_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        val_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        val_max = cv2.getTrackbarPos("Val Max", "TrackBars")

        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])

        # Create the mask from the image (Perform basic thresholding operations)
        mask = cv2.inRange(img_hsv, lower, upper)

        """ 
        Finding the circle 
        """

        mask_blur = cv2.medianBlur(mask, 7)  # mask already in grayscale

        param1 = cv2.getTrackbarPos("Sensitivity: Circles detection", "TrackBars")
        param2 = cv2.getTrackbarPos("Accuracy: Circles detection", "TrackBars")
        circles = cv2.HoughCircles(mask_blur, cv2.HOUGH_GRADIENT, 1, 100,
                                   param1=param1, param2=param2, minRadius=0, maxRadius=0)

        if circles is not None:
            detected_circles = np.uint16(circles).reshape((circles.shape[1], circles.shape[2]))

            # We want to filter all circles that was not close to the previous one

            closest_circle = None

            for circle in detected_circles:
                if closest_circle is None: closest_circle = circle
                if prev_circle is not None:

                    if np.linalg.norm(closest_circle[:2] - prev_circle[:2]) <= np.linalg.norm(
                            circle[:2] - prev_circle[:2]):
                        closest_circle = circle

            x_closet, y_closet, r_closet = closest_circle
            cv2.circle(img_copy, (x_closet, y_closet), r_closet, (0, 0, 255), 6)
            cv2.circle(img_copy, (x_closet, y_closet), 2, (0, 255, 255), 3)
            """ 
            # Since we have reflection on the light on the ball it generate sometimes additional circles
            # we only want to keep track of the largest circles detected

            circle_max = np.max(detected_circles, axis=0)
            x_max, y_max, r_max = circle_max
            cv2.circle(img_copy, (x_max, y_max), r_max, (255, 0, 0), 4)
            cv2.circle(img_copy, (x_max, y_max), 2, (0, 255, 255), 3)
            """

            prev_circle = closest_circle

            if print_all:
                for (x, y, r) in detected_circles:
                    # draw the outer circles
                    cv2.circle(img_copy, (x, y), r, (0, 255, 0), 2)
                    # draw the center of the circle
                    cv2.circle(img_copy, (x, y), 2, (0, 255, 255), 3)

        """ 
        Change the reference frame at the center
        """

        height, width, _ = img_copy.shape

        # Draw the cross at the center (overlay)
        cross_width = 2
        cv2.rectangle(img_copy, (0, int(height / 2) - cross_width), (width, int(height / 2) + cross_width), (255, 0, 0),
                      -1)
        cv2.rectangle(img_copy, (int(width / 2) - cross_width, 0), (int(width / 2) + cross_width, height), (255, 0, 0),
                      -1)

        # Change the ball position to a the reference frame
        if prev_circle is not None:
            x = prev_circle[0] - width / 2
            y = height / 2 - prev_circle[1]
            ball_pos = np.array([x, y])

        tolerance = 0.3

        t_x = tolerance * width / 2
        t_y = tolerance * height / 2

        # Check if the ball is left/center(ok)/right
        if prev_circle is not None:
            deviation = [0, 0]
            center=True
            if ball_pos[0] < -t_x:
                cv2.putText(img_copy, 'Left', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), thickness=3)
                center=False
            elif ball_pos[0] > t_x:
                cv2.putText(img_copy, 'Right', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), thickness=3)
                center = False

            if ball_pos[1] < -t_y:
                cv2.putText(img_copy, 'Bottom', (50, 90), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), thickness=3)
                center = False
            elif ball_pos[1] > t_y:
                cv2.putText(img_copy, 'Top', (50, 90), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), thickness=3)
                center = False
            if center:
                cv2.putText(img_copy, 'Center !', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), thickness=3)
        # Check if the ball in the the center of the frame (overlays)

        cv2.rectangle(img_copy, (int(width / 2 - t_x), int(height / 2 - t_y)),
                      (int(width / 2 + t_x), int(height / 2 + t_y)), (0, 255, 0),
                      2)

        frame_img = cv2.hconcat((img, img_copy))
        frame_mask = cv2.hconcat((mask, mask_blur))

        cv2.imshow("Mask with median blur applied", frame_mask)
        cv2.imshow("Image_with_balls", frame_img)

        if cv2.waitKey(1) == ord('e'):  # Press e to exit loop
            break

    return lower, upper, mask


# lower = np.array([37, 137, 26])
# upper = np.array([133, 255, 255])
find_blue_ball()
