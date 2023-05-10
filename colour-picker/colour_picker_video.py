import cv2 as cv

video = cv.VideoCapture("../input-videos/v_1_DNA.MP4")

# adjust wait time between frames
wait_time = 500

def nothing(x):
    pass

# Create a separate window for the color sliders
cv.namedWindow('Colour Sliders')
cv.moveWindow('Colour Sliders', 0, 0)

# Create the main window for displaying the result
cv.namedWindow('Colour Picker')
cv.moveWindow('Colour Picker', 0, 100)

# Create the sub window for displaying original image 
cv.namedWindow('Original')
cv.moveWindow('Original', 0, 100)

# Create trackbars in the color slider window
cv.createTrackbar('Min H', 'Colour Sliders', 35, 255, nothing)
cv.createTrackbar('Min S', 'Colour Sliders', 20, 255, nothing)
cv.createTrackbar('Min V', 'Colour Sliders', 50, 255, nothing)
cv.createTrackbar('Max H', 'Colour Sliders', 70, 255, nothing)
cv.createTrackbar('Max S', 'Colour Sliders', 255, 255, nothing)
cv.createTrackbar('Max V', 'Colour Sliders', 230, 255, nothing)

pause = False  # Flag to indicate if the video playback is paused

while True:
    if not pause:
      # Wait for a key press
      key = cv.waitKey(wait_time)
      if key & 0xFF == ord('q'):  # Quit if 'q' key is pressed
          break
      elif key & 0xFF == ord('n'):  # Pause/Resume if 'n' key is pressed
          pause = not pause

      frame_exists, frame = video.read()

      if not frame_exists:
          break

    # Get current trackbar values
    colour_min_h = cv.getTrackbarPos('Min H', 'Colour Sliders')
    colour_min_s = cv.getTrackbarPos('Min S', 'Colour Sliders')
    colour_min_v = cv.getTrackbarPos('Min V', 'Colour Sliders')
    colour_max_h = cv.getTrackbarPos('Max H', 'Colour Sliders')
    colour_max_s = cv.getTrackbarPos('Max S', 'Colour Sliders')
    colour_max_v = cv.getTrackbarPos('Max V', 'Colour Sliders')

    COLOUR_MIN = (colour_min_h, colour_min_s, colour_min_v)
    COLOUR_MAX = (colour_max_h, colour_max_s, colour_max_v)

    # Apply color filtering
    hsv_image = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    colour_mask = cv.inRange(hsv_image, COLOUR_MIN, COLOUR_MAX)
    result = cv.bitwise_and(frame, frame, mask=colour_mask)

    # Display the result
    print("Colour min: ", (colour_min_h, colour_min_s, colour_min_v))
    print("Colour max: ", (colour_max_h, colour_max_s, colour_max_v))
    cv.imshow('Colour Picker', result)
    cv.imshow('Original', frame)

    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):  # Quit if 'q' key is pressed
        break
    elif key & 0xFF == ord('n'):  # Pause/Resume if 'n' key is pressed
        pause = not pause

video.release()
cv.destroyAllWindows()
