import cv2
import numpy as np

# Define the callback function that will be called when the user clicks on the video frame
def on_mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the color of the clicked pixel
        color = frame[y, x]

        # Define the range of color tolerance
        tolerance = 30

        # Convert the color to HSV format
        hsv_color = cv2.cvtColor(color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds of the HSV range based on the selected pixel and color tolerance
        lower_bound = hsv_color - tolerance
        upper_bound = hsv_color + tolerance

        # Ensure that the values are within the valid range of 0-255 for HSV
        lower_bound = np.maximum(lower_bound, [0, 0, 0])
        upper_bound = np.minimum(upper_bound, [255, 255, 255])

        # Print the lower and upper bounds of the HSV range
        print("Lower Bound: [{}, {}, {}]".format(int(lower_bound[0, 0, 0]), int(lower_bound[0, 0, 1]), int(lower_bound[0, 0, 2])))
        print("Upper Bound: [{}, {}, {}]".format(int(upper_bound[0, 0, 0]), int(upper_bound[0, 0, 1]), int(upper_bound[0, 0, 2])))

# Create a VideoCapture object to read from a video file
cap = cv2.VideoCapture("../input-videos/red_yoyo.mp4")

# Loop over the video frames
while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If we've reached the end of the video, break out of the loop
    if not ret:
        break

    # Display the frame in a window named "video"
    cv2.imshow("video", frame)

    # Set the mouse callback function
    cv2.setMouseCallback("video", on_mouse_click)

    # Wait for a key press
    key = cv2.waitKey(5000) & 0xFF

    # If the 'q' key is pressed, break out of the loop
    if key == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
