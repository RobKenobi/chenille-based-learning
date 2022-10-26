import cv2
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



