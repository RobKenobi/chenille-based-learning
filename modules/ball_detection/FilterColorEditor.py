import cv2
import numpy as np


class FilterColorEditor:
    def __init__(self, video_feed=None, params=None):
        if params is None:
            params = {"lower": np.array([103, 154, 77]), "upper": np.array([170, 255, 255])}
        self._lower = params["lower"]
        self._upper = params["upper"]

        self._hue_min = self._lower[0]
        self._hue_max = self._upper[0]

        self._sat_min = self._lower[1]
        self._sat_max = self._upper[1]

        self._val_min = self._lower[2]
        self._val_max = self._upper[2]

        self._video_feed = cv2.VideoCapture(0) if video_feed is None else video_feed

    def update_params(self):
        self._hue_min = self._lower[0]
        self._hue_max = self._upper[0]

        self._sat_min = self._lower[1]
        self._sat_max = self._upper[1]

        self._val_min = self._lower[2]
        self._val_max = self._upper[2]

    def get_params(self):
        return {"upper": self._upper, "lower": self._lower}

    def set_params(self, params):
        self._lower = params["lower"]
        self._upper = params["upper"]
        self.update_params()

    def open_editor(self):
        def empty():
            pass

        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TrackBars", 640, 290)
        cv2.createTrackbar("Hue Min", "TrackBars", self._hue_min, 179, empty)
        cv2.createTrackbar("Hue Max", "TrackBars", self._hue_max, 179, empty)
        cv2.createTrackbar("Sat Min", "TrackBars", self._sat_min, 255, empty)
        cv2.createTrackbar("Sat Max", "TrackBars", self._sat_max, 255, empty)
        cv2.createTrackbar("Val Min", "TrackBars", self._val_min, 255, empty)
        cv2.createTrackbar("Val Max", "TrackBars", self._val_max, 255, empty)
        while True:

            success, img = self._video_feed.read()

            img_copy = img.copy()
            img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

            # Get the position of the tracker
            self._hue_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
            self._hue_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
            self._sat_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
            self._sat_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
            self._val_min = cv2.getTrackbarPos("Val Min", "TrackBars")
            self._val_max = cv2.getTrackbarPos("Val Max", "TrackBars")

            self._upper = np.array([self._hue_max, self._sat_max, self._val_max])
            self._lower = np.array([self._hue_min, self._sat_min, self._val_min])

            mask = cv2.inRange(img_hsv, self._lower, self._upper)

            cv2.imshow("Mask", mask)

            if cv2.waitKey(1) == ord("e"):
                params = self.get_params()
                cv2.destroyWindow("TrackBars")
                cv2.destroyWindow("Mask")
                return params
