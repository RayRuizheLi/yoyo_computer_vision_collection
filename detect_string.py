import cv2 as cv
import numpy as np
import math
import skvideo.io

video = cv.VideoCapture("vids/sinclair_blue_yoyo_green_string_bind.mp4")
fps = video.get(cv.CAP_PROP_FPS)

frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
#effect_video = cv.VideoWriter('string_detection.mp4', cv.VideoWriter_fourcc(*'mp4v'),fps, size)
vid_writer = skvideo.io.FFmpegWriter("string_detection.mp4")

GREEN_MIN = (35, 20, 50)
GREEN_MAX = (70, 255, 230)

def get_green_mask(img):
    hsv_image = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    green = cv.inRange(hsv_image, GREEN_MIN, GREEN_MAX)
    return green


print("Starting video processing...")
i = 0
while video.isOpened():
    isTrue, frame = video.read()
    if isTrue:
        i += 1
        if i % 50 == 0:
            print(i)
        green_pixels = get_green_mask(frame)
        vid_writer.writeFrame(green_pixels)
    else:
        break

video.release()
vid_writer.close()
cv.destroyAllWindows()
