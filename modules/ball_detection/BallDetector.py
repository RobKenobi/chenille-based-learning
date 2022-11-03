import cv2
import numpy as np


class BallDetector:
    def __init__(self, color_filter_params=None, circle_detector_params=None, sigma_blur=5):
        if color_filter_params is None:
            color_filter_params = {"lower": np.array([103, 154, 77]), "upper": np.array([170, 255, 255])}
        self._mask_lower = color_filter_params["lower"]
        self._mask_upper = color_filter_params["upper"]

        if circle_detector_params is None:
            circle_detector_params = {"minDist": 20, "param1": 50, "param2": 25, "minRadius": 0, "maxRadius": 0}

        self._minDist = circle_detector_params["minDist"]
        self._param1 = circle_detector_params["param1"]
        self._param2 = circle_detector_params["param2"]
        self._minRadius = circle_detector_params["minRadius"]
        self._maxRadius = circle_detector_params["maxRadius"]

        self.sigma_blur = sigma_blur

    def select_circle(self, circles):
        # TODO implement a strategy to select a circle if many are detected
        circle = None
        success = None
        return success, circle

    def detect_ball(self, image):
        img_copy = image.copy()
        img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(img_hsv, self._mask_lower, self._mask_upper)
        mask_blur = cv2.medianBlur(mask, 5)

        circles = cv2.HoughCircles(mask_blur, cv2.HOUGH_GRADIENT, 1, self._minDist,
                                   param1=self._param1, param2=self._param2, minRadius=self._minRadius,
                                   maxRadius=self._maxRadius)

        success, target = self.select_circle(circles)

        return success, target
