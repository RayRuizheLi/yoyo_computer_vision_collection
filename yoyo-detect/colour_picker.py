import cv2

# Define the callback function that will be called when the user clicks on the video frame
def on_mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the color of the clicked pixel
        color = frame[y, x]
        
        # Convert the color to HSV format
        hsv_color = cv2.cvtColor(color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV)

        # Print the color values in HSV format
        print("HSV color: {}".format(hsv_color))


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
