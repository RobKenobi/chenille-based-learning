import cv2
import numpy as np


class BallTracker:
    def __init__(self, height_reference=0.5, tolerance=0.3):
        # Position of the horizon (%) from top to bottom
        # 1   --> Horizon is the bottom of the image
        # 0.5 --> Horizon is in the middle of the image
        # 0   --> Horizon is the top of the image
        self._height_reference = height_reference

        # Tracker tolerance
        self._tolerance = tolerance

    def draw_cross(self, image):
        height, width, _ = image.shape

        # Draw the cross at the center (overlay)
        cross_width = 2
        cv2.rectangle(image, (0, int(height * self._height_reference) - cross_width),
                      (width, int(height * self._height_reference) + cross_width), (255, 0, 0), -1)

        cv2.rectangle(image, (int(width / 2) - cross_width, 0),
                      (int(width / 2) + cross_width, height), (255, 0, 0), -1)

        t_x = self._tolerance * width / 2
        t_y = self._tolerance * height / 2

        cv2.rectangle(image, (int(width / 2 - t_x), int(height * self._height_reference - t_y)),
                      (int(width / 2 + t_x), int(height *
                       self._height_reference + t_y)), (0, 255, 0),
                      2)

    def change_frame(self, circle, width, height):
        x = int(circle[0] - width / 2)
        y = int(height * self._height_reference - circle[1])
        ball_position = np.array([x, y])
        return ball_position

    def get_deviation(self, image, circle, true_deviation=False):
        # Retrieving image shape
        height, width, _ = image.shape

        # Computing the ball position in the reference frame
        x_circle, y_circle = self.change_frame(circle, width, height)

        if true_deviation:
            return np.array([x_circle, y_circle])

        t_x = self._tolerance * width / 2
        t_y = self._tolerance * height / 2

        deviation = np.array([0, 0])

        if y_circle < -t_y or y_circle > t_y:
            # We compute the deviation with the origin of the frame
            deviation[1] = y_circle

        if x_circle < -t_x or x_circle > t_x:
            deviation[0] = x_circle

        return deviation

    def display_position(self, image, circle, show_text=True):
        # Drawing the cross on the image
        self.draw_cross(image)

        # Showing the ball
        x_closet, y_closet, r_closet = circle
        cv2.circle(image, (x_closet, y_closet), r_closet, (0, 0, 255), 6)
        cv2.circle(image, (x_closet, y_closet), 2, (0, 255, 255), 3)

        deviation = self.get_deviation(image, circle)

        message = ""
        if deviation[1] > 0:
            message = "top "
        if deviation[1] < 0:
            message = "bottom "
        if deviation[0] > 0:
            message += "right"
        if deviation[0] < 0:
            message += "left"
        if message == "":
            message = "Center"

        # Show text with ball position
        if show_text:
            cv2.putText(image, message.capitalize(), (20, 20),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 0), thickness=1)

        return deviation
