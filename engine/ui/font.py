import pygame

from engine import utils

LINE_SPACING = 0.2  # relative to font size
KERNING = 0.4  # relative to font size

# Color cannot be (0,0,0) because I'm too lazy to fix a bug
class Font:
    def __init__(self, path, color=(255, 255, 255)):
        img = pygame.image.load(path).convert_alpha()
        self.chars: dict[str, pygame.Surface] = {}
        self.char_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-',
                           ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')',
                           '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        curr_w = 0
        img = utils.color_swap(img, (255, 0, 0), color)
        for x in range(img.get_width()):
            c = img.get_at((x, 0))
            if c[0] == 127:
                self.chars[self.char_order[len(self.chars)]] = utils.clip(img, pygame.Rect(x - curr_w, 0, curr_w,
                                                                                           img.get_height()))
                curr_w = 0
            else:
                curr_w += 1

    @property
    def kerning(self):
        return round(self.chars['A'].get_width() * KERNING)

    @property
    def line_height(self):
        return round(self.chars['A'].get_height() * (1 + LINE_SPACING))

    @property
    def standard_char_width(self):
        return self.chars['A'].get_width()

    def char_width(self, char, font_size=1):
        if char == "\n":
            return 0
        if char == " ":
            return self.standard_char_width * font_size
        return self.chars[char].get_width() * font_size

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
                curr_w += self.standard_char_width
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
                if curr_x != 0:
                    curr_x += self.chars['A'].get_width()
            else:
                surf.blit(self.chars[char], (curr_x, curr_y))
                curr_x += self.chars[char].get_width() + self.kerning
        surf.set_colorkey((0, 0, 0))
        return pygame.transform.scale(surf, (surf.get_width() * font_size, surf.get_height() * font_size))


def line_split_text(text: str, font: Font, font_size, max_width):
    line_indices = []
    recent_gap_i = 0
    tolerance = 10
    curr_w = 0
    for i in range(len(text)):
        char = text[i]

        if char == "\n":
            curr_w = 0
            continue

        if char == " ":
            recent_gap_i = i
        ch_w = font.text_bounds(char).width+font.kerning
        curr_w += ch_w
        if curr_w >= max_width:
            if i - recent_gap_i > tolerance:
                recent_gap_i = i
            line_indices.append(recent_gap_i)
            curr_w = 0

    for i in line_indices[::-1]:
        before = text[:i]
        after = text[i:]
        if not after.startswith(" "):
            before += "-"
        text = before + "\n" + after.removeprefix(" ")
    return text
