import cv2
import numpy as np


class BallDetector:
    def __init__(self, image_input):
        self._image_input = image_input

    def create_mask(self, params):
        self._upper = params["upper"]
        self._lower = params["lower"]


    def open_filter_color_editor(self):
        def empty():
            pass

        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TrackBars", 640, 290)
        cv2.createTrackbar("Hue Min", "TrackBars", 103, 179, empty)
        cv2.createTrackbar("Hue Max", "TrackBars", 170, 179, empty)
        cv2.createTrackbar("Sat Min", "TrackBars", 154, 255, empty)
        cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
        cv2.createTrackbar("Val Min", "TrackBars", 77, 255, empty)
        cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)
        cv2.createTrackbar("Param 1", "TrackBars", 50, 250, empty)
        cv2.createTrackbar("Param 2", "TrackBars", 25, 250, empty)

        while True:
            success, img = self._image_input.read()

            img_copy = img.copy()
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

            # Setting mask parameters
            self.mask_params = {"lower": lower, "upper": upper}

            # Creating mask 
            self.mask = cv2.inRange(img_hsv, lower, upper)

            # Press e to exit loop
            if cv2.waitKey(1) == ord('e'):
                break
