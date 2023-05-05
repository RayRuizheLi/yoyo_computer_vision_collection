import cv2 as cv
import numpy as np
import math
import skvideo.io

def nothing(x):
    pass

image = cv.imread("../input-videos/string.png")
cv.namedWindow('image')

cv.createTrackbar('Green Min H', 'image', 35, 255, nothing)
cv.createTrackbar('Green Min S', 'image', 20, 255, nothing)
cv.createTrackbar('Green Min V', 'image', 50, 255, nothing)

cv.createTrackbar('Green Max H', 'image', 70, 255, nothing)
cv.createTrackbar('Green Max S', 'image', 255, 255, nothing)
cv.createTrackbar('Green Max V', 'image', 230, 255, nothing)

while True:
    # Get current trackbar values
    green_min_h = cv.getTrackbarPos('Green Min H', 'image')
    green_min_s = cv.getTrackbarPos('Green Min S', 'image')
    green_min_v = cv.getTrackbarPos('Green Min V', 'image')
    green_max_h = cv.getTrackbarPos('Green Max H', 'image')
    green_max_s = cv.getTrackbarPos('Green Max S', 'image')
    green_max_v = cv.getTrackbarPos('Green Max V', 'image')
    
    GREEN_MIN = (green_min_h, green_min_s, green_min_v)
    GREEN_MAX = (green_max_h, green_max_s, green_max_v)
    
    # Apply color filtering
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    green_mask = cv.inRange(hsv_image, GREEN_MIN, GREEN_MAX)
    result = cv.bitwise_and(image, image, mask=green_mask)
    
    # Display the result
    cv.imshow('image', result)
    
    # Wait for a key press and check if the 'q' key was pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
