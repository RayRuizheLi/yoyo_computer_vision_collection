import sys
import os

# Add the parent directory to sys.path to allow imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import colour_filter_constants.colour_effect_constants as colour_effects
import colour_filter_constants.colour_HSV_constants as colour_values_HSV
import colour_filter as colour_filter
import colour_filter_settings 

BODY_SETTING_NAME = "Mono Colour YoYo Body Filter"
# Mono colour yoyo mp4 file was too big to upload to Github.
INPUT_PATH__FILTER_MONO_COLOUR_YOYO = "../input_videos/mono_colour_yoyo.MP4"
OUTPUT_PATH_FILTER_MONO_COLOUR_YOYO = "../intermediate_videos/mono_colour_yoyo_yoyo_filtered.MP4"
YOYO_BODY_HSV = colour_values_HSV.DOUBLE_FILTER_BODY_OF_MONO_COLOUR_PLASTIC_YOYO_HSV
BODY_EFFECT_TYPE = colour_filter_settings.FilterEffectTypes.SINGLE_COLOUR
BODY_EFFECT_SETTING = colour_filter_settings.SingleColourSetting(
    colour_effects.WHITE_BGR
)
BODY_IS_SHOW_FILTER_PROCESS = True

YOYO_BODY_COLOUR_FILTER_SETTING = colour_filter_settings.ColourFilterSetting(
    BODY_SETTING_NAME, 
    INPUT_PATH__FILTER_MONO_COLOUR_YOYO,
    OUTPUT_PATH_FILTER_MONO_COLOUR_YOYO,
    YOYO_BODY_HSV,
    BODY_EFFECT_TYPE,
    BODY_EFFECT_SETTING,
    BODY_IS_SHOW_FILTER_PROCESS
)

colour_filter.filter_colour(
    YOYO_BODY_COLOUR_FILTER_SETTING
)

STRING_SETTING_NAME = "Mono Colour YoYo String Filter"
YOYO_STRING_HSV = colour_values_HSV.DOUBLE_FILTER_STRING_OF_MONO_COLOUR_STRING_PLASTIC_YOYO_HSV
INPUT_PATH_FILTER_YOYO_STRING = "../intermediate_videos/mono_colour_yoyo_yoyo_filtered.MP4"
OUTPUT_PATH_FILTER_YOYO_STRING = "../output_videos/mono_colour_yoyo_yoyo_filtered_string_filtered.MP4"
STRING_EFFECT_TYPE = colour_filter_settings.FilterEffectTypes.SINGLE_COLOUR
STRING_EFFECT_SETTING = colour_filter_settings.SingleColourSetting(
    colour_effects.WHITE_BGR
)
STRING_IS_SHOW_FILTER_PROCESS = True

YOYO_STRING_COLOUR_FILTER_SETTING = colour_filter_settings.ColourFilterSetting(
    STRING_SETTING_NAME, 
    INPUT_PATH_FILTER_YOYO_STRING,
    OUTPUT_PATH_FILTER_YOYO_STRING,
    YOYO_STRING_HSV,
    STRING_EFFECT_TYPE,
    STRING_EFFECT_SETTING,
    STRING_IS_SHOW_FILTER_PROCESS
)

colour_filter.filter_colour(
    YOYO_STRING_COLOUR_FILTER_SETTING
)
