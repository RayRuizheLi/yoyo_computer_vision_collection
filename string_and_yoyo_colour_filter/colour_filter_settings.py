class ColourFilterSetting: 
    def __init__(self, setting_name, input_path, output_path, value_HSV, effect_colour, is_show_filter_process):
        self.setting_name = setting_name
        self.input_path = input_path
        self.output_path = output_path
        self.value_HSV = value_HSV
        self.effect_colour = effect_colour 
        self.is_show_filter_process = is_show_filter_process
        