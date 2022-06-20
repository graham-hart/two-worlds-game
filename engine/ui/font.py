import pygame

from .. import utils
from .style import Style


class Font:
    def __init__(self, path):
        img = pygame.image.load(path).convert_alpha()
        self.chars: dict[str, pygame.Surface] = {}
        self.char_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-',
                           ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')',
                           '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        curr_w = 0
        for x in range(img.get_width()):
            color = img.get_at((x, 0))
            if color[0] == 127:
                ch = utils.clip(img, pygame.Rect(x - curr_w, 0, curr_w, img.get_height()))
                if Style.FONT_COLOR is not None:
                    ch = utils.color_swap(ch, (255, 0, 0), Style.FONT_COLOR)
                self.chars[self.char_order[len(self.chars)]] = ch
                curr_w = 0
            else:
                curr_w += 1

    @property
    def kerning(self):
        return round(self.chars['A'].get_width() * Style.KERNING)

    @property
    def line_height(self):
        return round(self.chars['A'].get_height() * (1 + Style.LINE_SPACING))

    @property
    def char_width(self):
        return self.chars['A'].get_width()

    def text_bounds(self, text, font_size=1) -> pygame.Rect:
        curr_w = 0
        max_w = 0
        height = self.chars['A'].get_height()
        for char in text:
            if char == '\n':
                max_w = max(max_w, curr_w)
                curr_w = 0
                height += self.line_height
            elif char == ' ':
                curr_w += self.chars['A'].get_width()
            else:
                curr_w += self.chars[char].get_width() + self.kerning
        max_w = max(0, max(max_w, curr_w) - self.kerning)
        return pygame.Rect(0, 0, max_w * font_size, height * font_size)

    def render(self, text, font_size=1) -> pygame.Surface:
        bounds = self.text_bounds(text)
        surf = pygame.Surface(bounds.size)
        curr_x = 0
        curr_y = 0
        for char in text:
            if char == '\n':
                curr_y += self.line_height
                curr_x = 0
            elif char == ' ':
                curr_x += self.chars['A'].get_width()
            else:
                surf.blit(self.chars[char], (curr_x, curr_y))
                curr_x += self.chars[char].get_width() + self.kerning
        surf.set_colorkey((0,0,0))
        return pygame.transform.scale(surf, (surf.get_width() * font_size, surf.get_height() * font_size))
