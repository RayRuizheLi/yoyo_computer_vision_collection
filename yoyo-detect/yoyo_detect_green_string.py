import cv2 as cv
import numpy as np
import math
import skvideo.io

video = cv.VideoCapture("../input-videos/red_yoyo.mp4") # Works well for tiktok close ups! 
fps = video.get(cv.CAP_PROP_FPS)

frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
vid_writer = skvideo.io.FFmpegWriter("../output-videos/yoyo_detection.mp4")

COLOUR_MIN = (228, 116, 171)
COLOUR_MAX = (32, 176, 231)

#9 105 204
def get_green_mask(img):
    hsv_image = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    green = cv.inRange(hsv_image, COLOUR_MIN, COLOUR_MAX)
    return green


print("Starting video processing...")
i = 0
while video.isOpened():
    isTrue, frame = video.read()
    if isTrue:
        i += 1
        green_pixels = get_green_mask(frame)
        vid_writer.writeFrame(green_pixels)
    else:
        break

video.release()
vid_writer.close()
cv.destroyAllWindows()