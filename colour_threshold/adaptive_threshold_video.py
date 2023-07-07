import cv2

# Load input video
video = cv2.VideoCapture('../yoyo_contest.mp4')

# Create output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, 30, (640, 480))

while True:
    # Read a frame
    ret, frame = video.read()
    if not ret:
        break
        
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Write the frame to output video
    out.write(thresh)
    
    # Display the frame
    cv2.imshow('Output', thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and writer objects
video.release()
out.release()
cv2.destroyAllWindows()