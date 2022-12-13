import time

import cv2
import serial
from picamera import PiCamera
from picamera.array import PiRGBArray

from modules.ball_detection import BallDetector
from modules.ball_tracking import BallTracker

# Communication with Arduino
serialArduino = serial.Serial("/dev/ttyUSB0", 115200)

# Ball Detection
detector = BallDetector()

# Parameters for the ball tracker
tolerance = 0.3
height_reference = 0.5
# Ball tracker
tracker = BallTracker(height_reference=height_reference, tolerance=tolerance)

# Initialize the Pi camera
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# Wait for the camera to be ready
time.sleep(0.1)

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = rawCapture.array

        if image is not None:  # if an image is detected
            # Flipping image
            image = cv2.flip(image, -1)
            cv2.imwrite("test_image.png", image)
            # Trying to detect the ball
            success, target = detector.detect_ball(image)
            print(success)
            if success:
                deviation = tracker.get_deviation(image, target)
                radius = target[-1]

                # TODO : find the target radius
                target_radius = 10

                # TODO : find the reduction factor
                heading_error = deviation[1]
                distance_error = target_radius - radius

                # TODO : send infos to MQTT server
                # TODO : 
                # TODO : send the error to the arduino
        rawCapture.truncate()
        rawCapture.seek(0)

except KeyboardInterrupt:
    camera.close()
