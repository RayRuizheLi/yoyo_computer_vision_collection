import cv2
import numpy as np

# Load input video
video = cv2.VideoCapture('../yoyo_contest.mp4')

# Create output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, 30, (640, 480))

# Skip Past Unused Parts 
start_frame = 200

for i in range(start_frame):
    isTrue, frame = video.read()

while True:
    # Read a frame
    ret, frame = video.read()
    if not ret:
        break
        
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5,5), 0)


    # 11: This is the size of the neighborhood used for adaptive thresholding. In this case, 
    # it's set to 11, which means that the threshold value for each pixel is calculated based 
    # on the weighted sum of pixels in an 11x11 neighborhood around that pixel.

    # 2: This is a constant subtracted from the weighted sum of pixels in the neighborhood 
    # before calculating the threshold value. In this case, it's set to 2, which means 
    # that the threshold value is calculated as the weighted sum of pixels minus 2. 
    # This is often used to compensate for noise in the image.

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply connected component analysis to filter out regions that are not the yoyo string
    n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    yoyo_string_region = None
    max_area = 0
    min_area = 150 # set the minimum size of connected component to be considered as yoyo string
    for i in range(1, n_labels):
        if stats[i, cv2.CC_STAT_AREA] > max_area and stats[i, cv2.CC_STAT_AREA] > min_area:
            max_area = stats[i, cv2.CC_STAT_AREA]
            yoyo_string_region = labels == i

    # Erode the yoyo string region to separate it from the legs of the person
    kernel = np.ones((5, 5), np.uint8)
    yoyo_string_region = cv2.erode(yoyo_string_region.astype(np.uint8), kernel, iterations=3)

    # Convert the binary mask to uint8 and apply a bitwise_and operation with the original frame
    yoyo_string_region = yoyo_string_region.astype(np.uint8) * 255
    yoyo_string = cv2.bitwise_and(frame, frame, mask=yoyo_string_region)

    # Write the frame to output video
    out.write(yoyo_string)
    
    # Display the frame
    cv2.imshow('Output', yoyo_string)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and writer objects
video.release()
out.release()
cv2.destroyAllWindows()
