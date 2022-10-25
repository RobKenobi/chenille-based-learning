import cv2
import numpy as np


img = cv2.imread('image/2_circles.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


rows = gray.shape[0]

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT_ALT, 1, rows / 8,
                           param1=1, param2=0.9,
                           minRadius=1, maxRadius=30)
print(circles)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        # circle center
        cv2.circle(img, center, 1, (0, 255, 0), 3)
        # circle outline
        radius = i[2]
        cv2.circle(img, center, radius, (0, 255, 0), 3)

cv2.imshow("detected circles", img)
cv2.waitKey(0)