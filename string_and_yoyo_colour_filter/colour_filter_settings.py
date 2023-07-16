from enum import Enum
import colour_filter_constants.colour_effect_constants as colour_effects

class FilterEffectTypes(Enum):
    SINGLE_COLOUR = 1
    RAINBOW = 2

class SingleColourSetting:
    def __init__(self, effect_colour):
        self.effect_colour = effect_colour

class RainbowColourSetting:
    def __init__(self):
        self.effect_colours = [
            colour_effects.RED_BGR,
            colour_effects.ORANGE_BGR,
            colour_effects.YELLOW_BGR,
            colour_effects.GREEN_BGR,
            colour_effects.BLUE_BGR,
            colour_effects.INDIGO_BGR,
            colour_effects.VIOLET_BGR
        ]

class ColourFilterSetting: 
    def __init__(self, setting_name, input_path, output_path, value_HSV, effect_type, effect_setting, is_show_filter_process):
        self.setting_name = setting_name
        self.input_path = input_path
        self.output_path = output_path
        self.value_HSV = value_HSV
        self.effect_type = effect_type
        self.effect_setting = effect_setting 
        self.is_show_filter_process = is_show_filter_process
