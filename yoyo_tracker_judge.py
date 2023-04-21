import cv2 as cv 
import numpy as np
import math

# Modify the variables below to select behavior
save_tracking_video = True
save_effect_video = True
save_score_effect_video = True

# YoYo Effect Params 
num_effect_frames = 20 # how long the trail is
radius = 20
score_radius = 30
hue = 179 # Hue is between 0 and 179, could set to None. YoYo effect colour
score_hue = 200
saturation = 100 # Saturation is between 0 and 255


# Number of frames to fill in the gap between frames. default 5 
#   A bit surprised but this does not impact tracking but does 
#     seem to make video place faster if we lower it.
num_interpolation = 1 

# The first frame that will be used to select Region of Interst (ROI) # good value is 50. Cannot be 0
start_frame = 100 


# Read input video
video = cv.VideoCapture("input-videos/yoyo2.mp4")
fps = video.get(cv.CAP_PROP_FPS) 
print("FPS:",fps)
for i in range(start_frame):
    isTrue, frame = video.read()

# Tracker and bounding box initialization
# Works best when it is a giant bounding box 
tracker = cv.legacy.TrackerCSRT_create() 

# Testing where do we start to gather the frames for tracking 
bbox = cv.selectROI(frame, False)
ok = tracker.init(frame, bbox)
yoyo_locations = [(-1,-1)]*num_effect_frames # stores the (x,y) location of center of yoyo in a tuple.

# Set up output video
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)

if save_tracking_video:
    tracked_video = cv.VideoWriter('output-videos/tracking_video.mp4', cv.VideoWriter_fourcc(*'mp4v'),fps, size)
if save_effect_video:
    effect_video = cv.VideoWriter('output-videos/effect_video.mp4', cv.VideoWriter_fourcc(*'mp4v'),fps, size)
if save_score_effect_video:
    score_effect_video = cv.VideoWriter('output-videos/score_effect_video.mp4', cv.VideoWriter_fourcc(*'mp4v'),fps, size)


# Tracking velocity 
# Initialize values to -1 as a flag for no previous values
prev_x, prev_y = -1, -1
prev_velocity = -1
velocity_change_cap = 12
score = 0

# Helper Functions 
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def add_circle_effect_to_frame(target_frame, target_hue, target_saturation, is_score):
    # Calculate trail mask 
    trail_mask = np.full((frame_height, frame_width), False)
    circle_mask = np.full((frame_height, frame_width), False)

    cur_radius = 1

    if is_score:
        cur_radius = score_radius

    circle_yoyo_locations = interpolated_yoyo_locations

    # The back of the locations contains the most recent location
    #    we are only interested in the most recent valid position for scoring
    if is_score:
        circle_yoyo_locations = reversed(interpolated_yoyo_locations)

    for cx, cy, c_is_score in circle_yoyo_locations:
        if cx == -1 or cy == -1: 
            continue

        if is_score and not c_is_score:
            continue 

        Y, X = np.ogrid[:frame_height, :frame_width]
        dist_from_center = np.sqrt((X - cx)**2 + (Y - cy)**2)
        circle_mask = dist_from_center <= cur_radius
        trail_mask = np.logical_or(trail_mask, circle_mask)

        if is_score:
            break
        else:
            if cur_radius < radius:
                cur_radius += 1

    # Edit the pixel values
    if target_hue != None:
        target_frame[trail_mask, 0] = target_hue
    if target_saturation != None:
        target_frame[trail_mask, 1] = target_saturation

    # Make sure the range of values is between 0 and 225
    target_frame.clip(0,255)

    return target_frame


# Read each frame
while video.isOpened():

    isTrue, frame = video.read()
    if isTrue:

        ok,bbox=tracker.update(frame)
        effect_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        score_effect_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        
        if ok:
            (x,y,w,h)=[int(v) for v in bbox]
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            # Calculate Velocity 
            # distance/time and here time is 1
            # print("yoyo location: ", (x+w//2, y + h//2))
            is_location_score = False 
            if prev_x != -1:
                velocity = distance(prev_x, prev_y, x+w//2, y + h//2)
                print("yoyo velocity : ", velocity)

                if prev_velocity != -1:
                    velocity_change = abs(velocity - prev_velocity)
                    print("yoyo velocity change: ", velocity_change)

                    if velocity_change > velocity_change_cap:
                        is_location_score = True 
                        score += 1 
                        print("score! " + str(score))

                prev_velocity = velocity 
            
            prev_x, prev_y = x+w//2, y + h//2
            yoyo_locations.append((x+w//2, y + h//2, is_location_score))

            if len(yoyo_locations) == num_effect_frames + 1:
                yoyo_locations.pop(0)

            print("yoyo found")
        else:
            yoyo_locations.append((-1,-1))
            if len(yoyo_locations) == num_effect_frames + 1:
                yoyo_locations.pop(0)

            print("yoyo lost")
        
        # Insert more locations in between frames to make it more continuous
        interpolated_yoyo_locations = []
        for i, location in enumerate(yoyo_locations):
            if location ==  (-1,-1): continue

            # Find next valid location that is not (-1,-1)
            j = i+1
            if j >= len(yoyo_locations): break
            while j < len(yoyo_locations) and yoyo_locations[j] == (-1,-1) :
                j += 1
            if j >= len(yoyo_locations): break
            
            cur_x, cur_y, is_cur_score = location
            next_x, next_y, is_next_score = yoyo_locations[j]

            for step in range(num_interpolation+1):
                alpha = step * (1/num_interpolation)
                interpolated_x = int((1-alpha)*cur_x + (alpha * next_x))
                interpolated_y = int((1-alpha)*cur_y + (alpha * next_y))
                # Not sure if here should be cur score or next score
                interpolated_yoyo_locations.append((interpolated_x, interpolated_y, is_cur_score))

        # Create circle effects 
        effect_frame = add_circle_effect_to_frame(effect_frame, hue, saturation, False)
        score_effect_frame = add_circle_effect_to_frame(score_effect_frame, hue, saturation, True)

        
        # Add score 
        if save_score_effect_video:
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(score_effect_frame, "score: " + str(score), (50, 50), font, 1, (0, 255, 255), 2, cv.LINE_AA)

        # Show the video frames
        cv.imshow('Tracking Video', frame)
        effect_frame = cv.cvtColor(effect_frame, cv.COLOR_HSV2BGR)
        score_effect_frame = cv.cvtColor(score_effect_frame, cv.COLOR_HSV2BGR)
        cv.imshow('Effect Video', effect_frame)
        cv.imshow('Score Video', score_effect_frame)

        if cv.waitKey(20) & 0xFF==ord('q'):
            break 
        
        # save the video frames
        if save_tracking_video:
            tracked_video.write(frame)   

        if save_effect_video:
            effect_video.write(effect_frame)     

        if save_score_effect_video:
            score_effect_video.write(score_effect_frame)     
    else:
        break

video.release()
if save_tracking_video:  
    tracked_video.release()
if save_effect_video:
    effect_video.release()
cv.destroyAllWindows()