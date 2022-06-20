import pygame

from . import font


class SpeechBox:
    def __init__(self, img: pygame.Surface, sc_size: pygame.Vector2, text: str, fnt: font.Font, font_size: float, speed=0):
        self.img = img
        self.rect = img.get_rect()
        self.rect.move_ip((0, sc_size.y - self.rect.height))
        self.text = font.line_split_text(text, fnt, font_size, self.rect.width - 10)
        self.shown_text = ""
        self.speed = speed
        self.char_index = 0 if speed != 0 else len(self.text)
        self.font = fnt
        self.font_size = font_size

    def render(self, surf):
        text_surf = self.font.render(self.text[:self.char_index], self.font_size)
        surf.blit(self.img, self.rect)
        surf.blit(text_surf, self.rect.move(5, 5))

    def update(self):
        self.char_index += self.speed
        if self.char_index >= len(self.text):
            self.char_index = len(self.text)

    def set_text(self, text):
        self.char_index = 0
        self.text = font.line_split_text(text, self.font, self.font_size, self.rect.width - 10)
