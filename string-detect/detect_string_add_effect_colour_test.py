import cv2 as cv
import numpy as np
import skvideo.io

video = cv.VideoCapture("../input-videos/godspeed_trimmed.mp4")
fps = video.get(cv.CAP_PROP_FPS)
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
vid_writer = skvideo.io.FFmpegWriter("../output-videos/string_detection_effect.mp4")

GREEN_MIN = (35, 20, 50)
GREEN_MAX = (70, 255, 230)

def get_green_mask(img):
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    green = cv.inRange(hsv_image, GREEN_MIN, GREEN_MAX)
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
        result = cv.addWeighted(effect, 1, cv.cvtColor(mask, cv.COLOR_GRAY2BGR), 0.5, 0)
        vid_writer.writeFrame(result)
    else:
        break

video.release()
vid_writer.close()
cv.destroyAllWindows()
