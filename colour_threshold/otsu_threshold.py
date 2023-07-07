import cv2

# Load input image
img = cv2.imread('yoyoing.png')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Otsu's thresholding
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Display the output image
cv2.imshow('Output', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()