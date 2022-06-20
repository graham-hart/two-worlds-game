import pygame
import engine
from engine.input import Input, MouseButton
from .font import Font


PADDING = 5  # px
COLOR_1 = (0, 128, 255)
COLOR_2 = (100, 160, 255)

BUTTON_BORDER_RADIUS = 2
BUTTON_ELEVATION = 10
BORDER_WIDTH = 2

class Button:
    def __init__(self, text: str, pos: tuple[int, int], onclick: callable, font: Font,
                 font_size: float = None):
        self.text = text
        self.click = onclick
        self.pos = pos
        self.font = font
        self.text_surf = self.font.render(self.text, font_size)
        self.rect = pygame.Rect(self.pos, (
            self.text_surf.get_width() + PADDING * 2, self.text_surf.get_height() + PADDING * 2))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.elev_change = 0
        self.is_clicked = False

    def on_hover(self):
        pass

    def render(self, surf):
        pygame.draw.rect(surf, COLOR_1, self.rect.move(0, BUTTON_ELEVATION),
                         border_radius=BUTTON_BORDER_RADIUS)
        pygame.draw.rect(surf, COLOR_2, self.rect.move(0, self.elev_change),
                         border_radius=BUTTON_BORDER_RADIUS)
        surf.blit(self.text_surf, self.text_rect)

    def update(self):
        mouse_pos = Input.mouse_pos()
        mouse_state = Input.button_down(MouseButton.LEFT)
        in_rect = self.rect.collidepoint(mouse_pos) or self.rect.move(0,
                                                                      BUTTON_ELEVATION).collidepoint(mouse_pos)
        if self.is_clicked or not mouse_state or not in_rect:
            if (not mouse_state or not in_rect) and self.is_clicked:
                self.is_clicked = False
                self.text_rect.move_ip(0, -self.elev_change)
                self.elev_change = 0
                self.click()
            return False
        self.is_clicked = True
        self.elev_change = 5
        self.text_rect.move_ip(0, self.elev_change)
        return True

    @classmethod
    def centered(cls, text: str, pos, onclick: callable, font: Font,
                 font_size: float = None):
        font_size = font_size if font_size else 16
        text_size = font.text_bounds(text, font_size)
        pos = (pos[0] - text_size.width / 2 - PADDING, pos[1] - text_size.height / 2 - PADDING)
        return cls(text, pos, onclick, font, font_size)
