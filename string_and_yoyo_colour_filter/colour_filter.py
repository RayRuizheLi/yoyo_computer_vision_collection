import cv2 as cv
import numpy as np
import skvideo.io
from tqdm import tqdm

def filter_colour(colour_filter_setting):
    video = cv.VideoCapture(colour_filter_setting.input_path)
    vid_writer = skvideo.io.FFmpegWriter(colour_filter_setting.output_path)
    total_frames = int(video.get(cv.CAP_PROP_FRAME_COUNT))
    
    if colour_filter_setting.is_show_filter_process:
        create_window(colour_filter_setting.setting_name)

    for i in tqdm(range(total_frames), desc = generate_filter_description(colour_filter_setting.setting_name)):
        is_read_success, frame = video.read()

        if is_read_success:
            effect_result = generate_effect_result(frame, colour_filter_setting)
            
            if colour_filter_setting.is_show_filter_process:
                show_effect_result(colour_filter_setting, effect_result)

            vid_writer.writeFrame(effect_result)
            i += 1
        else:
            break

        # Required for effect to show in CV window
        if colour_filter_setting.is_show_filter_process:
            wait_for_effect_to_show()

    video.release()
    vid_writer.close()
    cv.destroyAllWindows()

def create_window(setting_name):
    cv.namedWindow(setting_name, cv.WINDOW_NORMAL)

def generate_filter_description(setting_name):
    return "Progress for " + setting_name

def generate_effect_result(frame, colour_filter_setting):
    colour_mask = generate_colour_mask(frame, colour_filter_setting.value_HSV)
    zeroed_colour_mask = generate_zeroed_contours_colour_mask(colour_mask)
    dilated_mask = generate_dilated_mask(zeroed_colour_mask)
    effect_mask = generate_effect_mask(dilated_mask, frame.shape, colour_filter_setting.effect_colour)

    effect = cv.addWeighted(frame, 1, effect_mask, 1, 0)
    effect_rgb = cv.cvtColor(effect, cv.COLOR_BGR2RGB)
    effect_result = cv.addWeighted(effect_rgb, 1, cv.cvtColor(dilated_mask, cv.COLOR_GRAY2BGR), 0.3, 0)

    return effect_result

def generate_colour_mask(img, colour_BGR):
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    colour_mask = cv.inRange(hsv_image, colour_BGR.colour_min, colour_BGR.colour_max)
    return colour_mask

def generate_zeroed_contours_colour_mask(colour_mask):
    contours = generate_contours(colour_mask)
    zeroed_colour_mask = np.zeros_like(colour_mask)
    cv.drawContours(zeroed_colour_mask, contours, -1, 255, 2)

    return zeroed_colour_mask

def generate_contours(colour_mask):            
    contours, _ = cv.findContours(colour_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    return contours

def generate_dilated_mask(mask):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    return cv.dilate(mask, kernel, iterations=1)

def generate_effect_mask(colour_mask, frame_shape, effect_colour):
    effect_mask = np.zeros(frame_shape, dtype=np.uint8)
    effect_mask[colour_mask == 255] = effect_colour
    return effect_mask

def show_effect_result(colour_filter_setting, effect_result):
    result_bgr = cv.cvtColor(effect_result, cv.COLOR_RGB2BGR)
    cv.imshow(colour_filter_setting.setting_name, result_bgr)

def wait_for_effect_to_show():
    WAIT_TIME_IN_MILLISECONDS = 1
    cv.waitKey(WAIT_TIME_IN_MILLISECONDS)