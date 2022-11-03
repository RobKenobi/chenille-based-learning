import cv2
import numpy as np

# TODO test it

class CircleDetectorEditor:
    def __init__(self, video_feed=None, circle_params=None, mask_params=None, sigma_blur=5):

        self._video_feed = cv2.VideoCapture(0) if video_feed is None else video_feed

        if circle_params is None:
            circle_params = {"minDist": 20, "param1": 50, "param2": 25, "minRadius": 0, "maxRadius": 0}

        self._minDist = circle_params["minDist"]
        self._param1 = circle_params["param1"]
        self._param2 = circle_params["param2"]
        self._minRadius = circle_params["minRadius"]
        self._maxRadius = circle_params["maxRadius"]

        if mask_params is None:
            mask_params = {"lower": np.array([103, 154, 77]), "upper": np.array([170, 255, 255])}

        self._mask_lower = mask_params["lower"]
        self._mask_upper = mask_params["upper"]

        self._sigma_blur = sigma_blur

    def get_params(self):
        return {"minDist": self._minDist, "param1": self._param1, "param2": self._param2, "minRadius": self._minRadius,
                "maxRadius": self._maxRadius}

    def open_editor(self):
        def empty(x):
            pass

        cv2.namedWindow("TrackBars : Circle detection")
        cv2.resizeWindow("TrackBars : Circle detection", 640, 290)
        cv2.createTrackbar("minDist", "TrackBars : Circle detection", self._minDist, 250, empty)
        cv2.createTrackbar("param1", "TrackBars : Circle detection", self._param1, 250, empty)
        cv2.createTrackbar("param2", "TrackBars : Circle detection", self._param2, 250, empty)
        cv2.createTrackbar("minRadius", "TrackBars : Circle detection", self._minRadius, 250, empty)
        cv2.createTrackbar("maxRadius", "TrackBars : Circle detection", self._maxRadius, 250, empty)

        while True:
            success, img = self._video_feed.read()

            img_copy = img.copy()
            img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(img_hsv, self._mask_lower, self._mask_upper)
            mask_blur = cv2.medianBlur(mask, 5)

            self._minDist = cv2.getTrackbarPos("minDist", "TrackBars : Circle detection")
            self._param1 = cv2.getTrackbarPos("param1", "TrackBars : Circle detection")
            self._param2 = cv2.getTrackbarPos("param2", "TrackBars : Circle detection")
            self._minRadius = cv2.getTrackbarPos("minRadius", "TrackBars : Circle detection")
            self._maxRadius = cv2.getTrackbarPos("maxRadius", "TrackBars : Circle detection")

            circles = cv2.HoughCircles(mask_blur, cv2.HOUGH_GRADIENT, 1, self._minDist,
                                       param1=self._param1, param2=self._param2, minRadius=self._minRadius,
                                       maxRadius=self._maxRadius)

            if circles is not None:
                detected_circles = np.uint16(circles).reshape((circles.shape[1], circles.shape[2]))

                for (x, y, r) in detected_circles:
                    # draw the outer circles
                    print(x, y, r)
                    cv2.circle(img_copy, (x, y), r, (0, 255, 0), 2)
                    # draw the center of the circle
                    cv2.circle(img_copy, (x, y), 2, (0, 255, 255), 3)
            else:
                print("No circle detected")

            cv2.imshow("Circle detector", img_copy)

            # Press "e" to exit
            if cv2.waitKey(1) == ord("e"):
                # Closing windows
                cv2.destroyAllWindows()

                # Returning parameters
                params = self.get_params()
                return params
