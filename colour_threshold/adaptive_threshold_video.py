import cv2

# Load input video
video = cv2.VideoCapture('../yoyo_contest.mp4')

# Get video properties
fps = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Create output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))

while True:
    # Read a frame
    ret, frame = video.read()
    if not ret:
        break
        
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Write the frame to output video
    out.write(thresh)
    
    # Display the frame
    cv2.waitKey(25)  # Add delay of 25ms per frame

    cv2.imshow('Output', thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and writer objects
video.release()
out.release()

# Close all windows
cv2.destroyAllWindows()