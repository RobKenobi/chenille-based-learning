import time

import cv2

from modules.aruco import ArucoDetector

# import serial

# Communication with Arduino
# serialArduino = serial.Serial("/dev/ttyUSB0", 115200)

# Aruco Detection
detector = ArucoDetector()

# Video feed
cap = cv2.VideoCapture(0)

# Wait for the camera to be ready
time.sleep(0.1)

last_time = time.time()

while True:
    # Press <ESC>
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break

    # Getting image from camera
    ret, image = cap.read()

    if ret:
        # Flipping image
        image = cv2.flip(image, -1)

        # Convert BRG image to GRAY image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Trying to detect the ball
        success, *_ = detector.detection(gray)

        if success and time.time() - last_time > 0.5:
            heading_error, distance_error = detector.get_deviation()
            heading_error /= 20
            distance_error /= 100
            servo = 0

            message = f"Distance error : {distance_error}\nHeading error : {heading_error}\nServo : {servo}"
            print(10 * "---")
            print(message)

            message_to_send = f"{distance_error};{heading_error};{servo}\n"
            # serialArduino.write(message_to_send.encode())
            last_time = time.time()

        cv2.imshow("Image", image)
