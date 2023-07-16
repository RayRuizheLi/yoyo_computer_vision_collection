import sys
import os

# Add the parent directory to sys.path to allow imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import colour_filter_constants.colour_effect_constants as colour_effects
import colour_filter_constants.colour_HSV_constants as colour_values_HSV
import colour_filter as colour_filter
import colour_filter_settings

SETTING_NAME = "Rainbow Effect Godspeed"
INPUT_PATH__GOD_SPEED_TRIMMED = "../input_videos/godspeed_trimmed.mp4"
OUTPUT_PATH_GOD_SPEED_TRIMMED = "../output_videos/rainbow_godspeed_trimmed.MP4"
GODSPEED_HSV = colour_values_HSV.GODSPEED_HSV
GODSPEED_EFFECT_TYPE = colour_filter_settings.FilterEffectTypes.RAINBOW
GODSPEED_EFFECT_SETTING = colour_filter_settings.RainbowColourSetting()
IS_SHOW_FILTER_PROCESS = True

RAINBOW_EFFECT_GODSPEED_COLOUR_FILTER_SETTING = colour_filter_settings.ColourFilterSetting(
    SETTING_NAME, 
    INPUT_PATH__GOD_SPEED_TRIMMED,
    OUTPUT_PATH_GOD_SPEED_TRIMMED,
    GODSPEED_HSV,
    GODSPEED_EFFECT_TYPE,
    GODSPEED_EFFECT_SETTING,
    IS_SHOW_FILTER_PROCESS
)

colour_filter.filter_colour(
    RAINBOW_EFFECT_GODSPEED_COLOUR_FILTER_SETTING
)