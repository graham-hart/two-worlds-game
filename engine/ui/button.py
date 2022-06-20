from typing import Optional

import pygame

from .. import ui
from .style import Style


class Button:
    def __init__(self, text: str, pos: tuple[int, int], onclick: callable, font: Optional[str] = None,
                 font_size: float = None):
        self.text = text
        self.click = onclick
        self.pos = pos
        font_size = font_size if font_size else Style.REGULAR_FONT_SIZE
        self.font = Style.FONT if not font else Style.get_font(font)
        self.text_surf = self.font.render(self.text, font_size)
        self.rect = pygame.Rect(self.pos, (
            self.text_surf.get_width() + Style.PADDING * 2, self.text_surf.get_height() + Style.PADDING * 2))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.elev_change = 0
        self.is_clicked = False

    def on_hover(self):
        pass

    def render(self, surf):
        pygame.draw.rect(surf, Style.COLOR_1, self.rect.move(0, Style.BUTTON_ELEVATION),
                         border_radius=Style.BUTTON_BORDER_RADIUS)
        pygame.draw.rect(surf, Style.COLOR_2, self.rect.move(0, self.elev_change),
                         border_radius=Style.BUTTON_BORDER_RADIUS)
        surf.blit(self.text_surf, self.text_rect)

    def check_click(self, mouse_pos, mouse_state):
        in_rect = self.rect.collidepoint(mouse_pos) or self.rect.move(0,
                                                                      Style.BUTTON_ELEVATION).collidepoint(mouse_pos)
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

    # def update(self, evts):


    @classmethod
    def centered(cls, text: str, pos, onclick: callable, font: Optional[str] = None,
                 font_size: float = None):
        fnt: ui.Font = Style.FONT if not font else Style.get_font(font)
        font_size = font_size if font_size else Style.REGULAR_FONT_SIZE
        text_size = fnt.text_bounds(text, font_size)
        pos = (pos[0] - text_size.width / 2 - Style.PADDING, pos[1] - text_size.height / 2 - Style.PADDING)
        return cls(text, pos, onclick, font, font_size)
