# Code Written by ChatGPT that does not work

import cv2 as cv 

# Read input video
video = cv.VideoCapture("yoyo2.mp4")
fps = video.get(cv.CAP_PROP_FPS) 
print("FPS:",fps)

# Define KCF tracker
tracker = cv.TrackerKCF_create()

# Select ROI
while True:
    ret, frame = video.read()
    if not ret:
        break
    cv.imshow("Select ROI", frame)
    k = cv.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('r'):
        bbox = cv.selectROI(frame, False)
        ok = tracker.init(frame, bbox)
        break

# Set up output video
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
tracked_video = cv.VideoWriter('tracking_video.mp4', cv.VideoWriter_fourcc(*'XVID'),fps, size)

# Read each frame
while video.isOpened():

    isTrue, frame = video.read()
    if isTrue:

        # Update tracker and draw bounding box
        ok,bbox = tracker.update(frame)
        if ok:
            (x,y,w,h)=[int(v) for v in bbox]
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        # Show and save video frame
        cv.imshow('Tracking Video', frame)
        tracked_video.write(frame)

        if cv.waitKey(20) & 0xFF==ord('q'):
            break 
        
    else:
        break

video.release()
tracked_video.release()
cv.destroyAllWindows()
