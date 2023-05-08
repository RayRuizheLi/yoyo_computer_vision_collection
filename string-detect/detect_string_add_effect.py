import cv2 as cv
import numpy as np
import skvideo.io

video = cv.VideoCapture("../input-videos/godspeed_trimmed.mp4")
fps = video.get(cv.CAP_PROP_FPS)
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
vid_writer = skvideo.io.FFmpegWriter("../output-videos/string_detection_effect.mp4")
cv.namedWindow('String Effect')

COLOUR_MIN = (35, 20, 50)
COLOUR_MAX = (70, 255, 230)

# BGR format
white_effect = (255, 255, 255)
blue_effect = (255, 0, 0)
green_effect = (0, 255, 0)
red_effect = (0, 0, 255)
custom_effect = (0, 50, 255)


# Pick the colour effect you want
colour_effect = blue_effect

def get_colour_mask(img):
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    colour = cv.inRange(hsv_image, COLOUR_MIN, COLOUR_MAX)
    return colour

print("Starting video processing...")
i = 0
while video.isOpened():
    isTrue, frame = video.read()
    if isTrue:
        i += 1
        colour_mask = get_colour_mask(frame)
        contours, hierarchy = cv.findContours(colour_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        mask = np.zeros_like(colour_mask)
        cv.drawContours(mask, contours, -1, 255, 2)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        mask = cv.dilate(mask, kernel, iterations=1)
        colour_mask = np.zeros(frame.shape, dtype=np.uint8)
        colour_mask[mask == 255] = colour_effect
        effect = cv.addWeighted(frame, 1, colour_mask, 1, 0)
        effect_rgb = cv.cvtColor(effect, cv.COLOR_BGR2RGB)
        result = cv.addWeighted(effect_rgb, 1, cv.cvtColor(mask, cv.COLOR_GRAY2BGR), 0.3, 0)

        result_bgr = cv.cvtColor(result, cv.COLOR_RGB2BGR)
        cv.imshow('String Effect', result_bgr)
        vid_writer.writeFrame(result)
        
        # Wait for a key press and check if the 'q' key was pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

video.release()
vid_writer.close()
cv.destroyAllWindows()
