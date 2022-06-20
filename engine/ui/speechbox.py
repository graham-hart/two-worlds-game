import pygame

from . import font


class SpeechBox:
    def __init__(self, img: pygame.Surface, sc_size: pygame.Vector2, text: str, fnt: font.Font, font_size: float):
        self.img = img
        self.rect = img.get_rect()
        self.rect.move_ip((0, sc_size.y - self.rect.height))
        self.text = font.line_split_text(text, fnt, font_size, sc_size.x - 10)
        self.shown_text = ""
        self.char_index = 0
        self.font = fnt
        self.font_size = font_size

    def render(self, surf):
        text_surf = self.font.render(self.shown_text, self.font_size)
        surf.blit(self.img, self.rect)
        surf.blit(text_surf, self.rect.move(5, 5))

    def update(self):
        if len(self.shown_text) < len(self.text):
            self.shown_text += self.text[self.char_index]
            self.char_index += 1
