import cv2 as cv
import numpy as np
import skvideo.io

video = cv.VideoCapture("../input-videos/demon_speed_trimmed.mp4")
fps = video.get(cv.CAP_PROP_FPS)
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
vid_writer = skvideo.io.FFmpegWriter("../output-videos/yoyo_detection_effect.mp4")

COLOUR_MIN = (5, 80, 100)
COLOUR_MAX = (25, 255, 255)

def get_green_mask(img, lower_range, upper_range):
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_image, lower_range, upper_range)
    return mask

def on_min_hue(val):
    global COLOUR_MIN
    COLOUR_MIN = (val, COLOUR_MIN[1], COLOUR_MIN[2])
    
def on_max_hue(val):
    global COLOUR_MAX
    COLOUR_MAX = (val, COLOUR_MAX[1], COLOUR_MAX[2])
    
def on_min_sat(val):
    global COLOUR_MIN
    COLOUR_MIN = (COLOUR_MIN[0], val, COLOUR_MIN[2])
    
def on_max_sat(val):
    global COLOUR_MAX
    COLOUR_MAX = (COLOUR_MAX[0], val, COLOUR_MAX[2])
    
def on_min_val(val):
    global COLOUR_MIN
    COLOUR_MIN = (COLOUR_MIN[0], COLOUR_MIN[1], val)
    
def on_max_val(val):
    global COLOUR_MAX
    COLOUR_MAX = (COLOUR_MAX[0], COLOUR_MAX[1], val)

cv.namedWindow('Adjust Color Range')
cv.createTrackbar('Min Hue', 'Adjust Color Range', COLOUR_MIN[0], 180, on_min_hue)
cv.createTrackbar('Max Hue', 'Adjust Color Range', COLOUR_MAX[0], 180, on_max_hue)
cv.createTrackbar('Min Saturation', 'Adjust Color Range', COLOUR_MIN[1], 255, on_min_sat)
cv.createTrackbar('Max Saturation', 'Adjust Color Range', COLOUR_MAX[1], 255, on_max_sat)
cv.createTrackbar('Min Value', 'Adjust Color Range', COLOUR_MIN[2], 255, on_min_val)
cv.createTrackbar('Max Value', 'Adjust Color Range', COLOUR_MAX[2], 255, on_max_val)



def get_green_mask(img):
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    green = cv.inRange(hsv_image, COLOUR_MIN, COLOUR_MAX)
    return green

print("Starting video processing...")
i = 0
while video.isOpened():
    isTrue, frame = video.read()
    if isTrue:
        i += 1
        green_mask = get_green_mask(frame)
        contours, hierarchy = cv.findContours(green_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        mask = np.zeros_like(green_mask)
        cv.drawContours(mask, contours, -1, 255, 2)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        mask = cv.dilate(mask, kernel, iterations=1)
        white_mask = np.zeros(frame.shape, dtype=np.uint8)
        white_mask[mask == 255] = (255, 255, 255)
        effect = cv.addWeighted(frame, 0.7, white_mask, 0.3, 0)
        # result = cv.addWeighted(effect, 1, cv.cvtColor(mask, cv.COLOR_GRAY2BGR), 0.5, 0)
        effect_rgb = cv.cvtColor(effect, cv.COLOR_BGR2RGB)
        result = cv.addWeighted(effect_rgb, 1, cv.cvtColor(mask, cv.COLOR_GRAY2BGR), 0.5, 0)
        vid_writer.writeFrame(result)
    else:
        break

video.release()
vid_writer.close()
cv.destroyAllWindows()