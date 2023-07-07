class ColourFilterValueHSV:
    def __init__(self, colour_min=(0, 0, 0), colour_max=(0, 0, 0), applicable_videos=[]):
        self.colour_min = colour_min
        self.colour_max = colour_max
        self.applicable_videos = applicable_videos
