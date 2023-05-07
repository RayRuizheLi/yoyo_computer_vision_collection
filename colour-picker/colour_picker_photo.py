import cv2 as cv
import numpy as np
import math
import skvideo.io

def nothing(x):
    pass

image = cv.imread("../input-videos/string.png")
cv.namedWindow('Colour Picker')

cv.createTrackbar('Min H', 'image', 35, 255, nothing)
cv.createTrackbar('Min S', 'image', 20, 255, nothing)
cv.createTrackbar('Min V', 'image', 50, 255, nothing)

cv.createTrackbar('Max H', 'image', 70, 255, nothing)
cv.createTrackbar('Max S', 'image', 255, 255, nothing)
cv.createTrackbar('Max V', 'image', 230, 255, nothing)

while True:
    # Get current trackbar values
    colour_min_h = cv.getTrackbarPos('Min H', 'image')
    colour_min_s = cv.getTrackbarPos('Min S', 'image')
    colour_min_v = cv.getTrackbarPos('Min V', 'image')
    colour_max_h = cv.getTrackbarPos('Max H', 'image')
    colour_max_s = cv.getTrackbarPos('Max S', 'image')
    colour_max_v = cv.getTrackbarPos('Max V', 'image')
    
    COLOUR_MIN = (colour_min_h, colour_min_s, colour_min_v)
    COLOUR_MAX = (colour_max_h, colour_max_s, colour_max_v)
    
    # Apply color filtering
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    colour_mask = cv.inRange(hsv_image, COLOUR_MIN, COLOUR_MAX)
    result = cv.bitwise_and(image, image, mask=colour_mask)
    
    # Display the result
    cv.imshow('image', result)
    
    # Wait for a key press and check if the 'q' key was pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
