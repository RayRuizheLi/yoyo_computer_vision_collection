import cv2
import numpy as np

# Create a black image
img = np.zeros((300,512,3), np.uint8)

# Create a window
cv2.namedWindow('image')

# Create a callback function for the trackbar
def nothing(x):
    pass

# Create a trackbar
cv2.createTrackbar('Value', 'image', 0, 255, nothing)

while True:
    # Get the current trackbar value
    value = cv2.getTrackbarPos('Value', 'image')

    # Draw a line with the current trackbar value
    cv2.line(img,(0,0),(511,300),(value,0,255),5)

    # Display the image
    cv2.imshow('image',img)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
