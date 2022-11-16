import cv2
import numpy as np


class BallDetector:
    def __init__(self, color_filter_params=None, circle_detector_params=None, sigma_blur=5):
        if color_filter_params is None:
            color_filter_params = {"lower": np.array([55, 158, 77]), "upper": np.array([128, 255, 255])}
        self._mask_lower = color_filter_params["lower"]
        self._mask_upper = color_filter_params["upper"]

        if circle_detector_params is None:
            circle_detector_params = {"minDist": 250, "param1": 50, "param2": 11, "minRadius": 0, "maxRadius": 0}

        self._minDist = circle_detector_params["minDist"]
        self._param1 = circle_detector_params["param1"]
        self._param2 = circle_detector_params["param2"]
        self._minRadius = circle_detector_params["minRadius"]
        self._maxRadius = circle_detector_params["maxRadius"]

        self.sigma_blur = sigma_blur

        self._prev_circle = None

    def select_circle(self, circles):
        if circles is None:
            return False, None

        # Convert circles into a numpy array
        circles = np.uint16(circles).reshape((circles.shape[1], circles.shape[2]))

        if self._prev_circle is None:
            self._prev_circle = circles[0]

        # Compute the distances between the previous circles and the detected ones
        distance = np.linalg.norm(circles[:, :2] - self._prev_circle[:2], axis=1)
        sorted_index = np.argsort(distance)

        # Sort the detected circles by their distance to the previous circle
        sorted_circles = circles[sorted_index]

        # Keep the first circle
        circle = sorted_circles[0]

        self._prev_circle = circle
        success = True
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
