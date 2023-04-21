import cv2
import numpy as np

# Load input image
img = cv2.imread('yoyoing.png')

# Convert to HSV color space
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define range of yellow color in HSV
lower_yellow = np.array([0, 0, 0])
upper_yellow = np.array([40, 255, 255])

# Threshold the HSV image to get only yellow colors
mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

# Apply morphology operations to clean up the binary mask
kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Apply the mask to the input image
output = cv2.bitwise_and(img, img, mask=mask)

# Display the output image
cv2.imshow('Output', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
