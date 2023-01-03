import time

import cv2
import numpy as np

# Define the chess board rows and columns
rows = 7  # TODO : Select the right number of rows
cols = 10  # TODO : Select the right number of columns
square_size = 20  # TODO : Set the square size in mm

# Set the termination criteria for the corner sub-pixel algorithm
criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)

# Prepare the object points: (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0). They are the same for all images
objectPoints = np.zeros((rows * cols, 3), np.float32)
objectPoints[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2) * square_size

# Create the arrays to store the object points and the image points
objectPointsArray = []
imgPointsArray = []

cap = cv2.VideoCapture(0)
time.sleep(1)

nb_image = 10
stop_good_image = nb_image  # number of chessboard detection

start = time.time()

# Loop over the image files
while True:
    key = cv2.waitKey(1)

    # Load the image and convert it to gray scale
    _, img = cap.read()
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (rows, cols), None)

    # Make sure the chess board pattern was found in the image
    if ret:
        # Refine the corner position
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        if time.time() - start > 3:
            stop_good_image -= 1
            start = time.time()

            # Add the object points and the image points to the arrays
            objectPointsArray.append(objectPoints)
            imgPointsArray.append(corners)

        # Draw the corners on the image
        cv2.drawChessboardCorners(img, (rows, cols), corners, ret)

    print("\rProgression : ", round((1 - stop_good_image / nb_image) * 100), " %", end='')

    # Display the image
    cv2.imshow('chess board', img)

    if key == 27 or stop_good_image == 0:
        print("\nFinished")
        break

    # TODO : Check we have enough board pattern detection (like at least 50) before continue
    # Continue == stopping the loop

# Calibrate the camera and save the results
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPointsArray, imgPointsArray, gray.shape[::-1], None, None)

# TODO : Print the result and write it down on a paper

# Print the camera calibration error
error = 0

for i in range(len(objectPointsArray)):
    imgPoints, _ = cv2.projectPoints(objectPointsArray[i], rvecs[i], tvecs[i], mtx, dist)
    error += cv2.norm(imgPointsArray[i], imgPoints, cv2.NORM_L2) / len(imgPoints)

print("Total error: ", error / len(objectPointsArray))

# Load the last images
h, w = img.shape[:2]

# Obtain the new camera matrix and undistort the image
newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
undistortedImg = cv2.undistort(img, mtx, dist, None, newCameraMtx)

# Crop the undistorted image
# x, y, w, h = roi
# undistortedImg = undistortedImg[y:y + h, x:x + w]

# Display the final result
cv2.imshow('chess board', np.hstack((img, undistortedImg)))
cv2.waitKey(0)
cv2.destroyAllWindows()

# Ask whether to save the data
choice = input("Save matrix ? (y/n) ")
# Save the data if positive answer
if choice == "y":
    np.save("mtx.npy", mtx)
    np.save("dist.npy", dist)
