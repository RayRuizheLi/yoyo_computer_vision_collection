import cv2

# Load the input image in grayscale
img = cv2.imread('yoyoing.png', 0)

# Apply Gaussian blur to reduce noise
img = cv2.GaussianBlur(img, (5,5), 0)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Show the thresholded image
cv2.imshow('Thresholded Image', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()