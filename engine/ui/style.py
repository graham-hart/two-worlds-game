import os

from engine import ui


class Style:
    LINE_SPACING = 0.2  # relative to font size
    KERNING = 0.4  # relative to font size
    FONT_COLOR = (255, 255, 255)
    PADDING = 5  # px
    FONTS = {}
    FONT = None
    REGULAR_FONT_SIZE = 2
    SMALL_FONT_SIZE = 0.5
    LARGE_FONT_SIZE = 2.5
    XL_FONT_SIZE = 5
    BUTTON_BORDER_RADIUS = 2
    BUTTON_ELEVATION = 10
    BORDER_WIDTH = 2

    COLOR_1 = (0, 128, 255)
    COLOR_2 = (100, 160, 255)

    @staticmethod
    def load_font(font_path):
        Style.FONT = ui.Font(font_path)
        Style.FONTS[os.path.splitext(os.path.split(font_path)[-1])[0]] = Style.FONT
        return Style.FONT

    @staticmethod
    def get_font(font_name):
        return Style.FONTS[font_name]
