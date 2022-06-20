from typing import Optional

import pygame

from .. import utils
from .style import Style


class TextInput:
    def __init__(self, pos: tuple[int, int], width: int, font: Optional[str] = None,
                 font_size: float = None, dynamic_width: bool = True, placeholder: str = "", on_enter: callable=None):
        self.placeholder = placeholder
        self.width = width  # If dynamic width, this is the minimum width of input box (not including padding)
        self.dynamic_width = dynamic_width
        self.pos = pos
        self.font_size = font_size if font_size else Style.REGULAR_FONT_SIZE
        self.font = Style.FONT if not font else Style.get_font(font)
        self.rect = pygame.Rect(
            (pos[0], pos[1], self.width + Style.PADDING * 2,
             self.font.chars['A'].get_height() * self.font_size + Style.PADDING * 2))
        self.selected = False
        self.left = ""
        self.right = ""
        self.repeat_delay = 100
        self.repeat_timeout = 500
        self.pressed = {}
        self._process_return = on_enter if on_enter else lambda: None

    @property
    def text(self):
        return self.left + self.right

    @text.setter
    def text(self, txt):
        cursor = self.cursor_pos
        self.left = txt[:cursor]
        self.right = txt[cursor:]

    @property
    def cursor_pos(self):
        return len(self.left)

    def toggle_select(self):
        self._process_end()
        self.selected = not self.selected

    @cursor_pos.setter
    def cursor_pos(self, pos):
        pos = utils.clamp(pos, 0, len(self.text))
        full = self.text
        self.left = full[:pos]
        self.right = full[pos:]

    @property
    def cursor_pixel_pos(self):
        size = self.font.text_bounds(self.left, self.font_size)[2]
        return size if self.dynamic_width else min(size, self.width)

    def update_rect(self):
        if self.dynamic_width:
            width = max(self.font.text_bounds(self.text if len(self.text) else self.placeholder, self.font_size)[2],
                        self.width)
            self.rect.update(self.rect.topleft, (width + Style.PADDING * 2, self.rect.height))

    def render(self, surf):
        self.update_rect()
        pygame.draw.rect(surf, Style.COLOR_2, self.rect, border_radius=Style.BUTTON_BORDER_RADIUS)
        pygame.draw.rect(surf, Style.COLOR_1, self.rect, width=Style.BORDER_WIDTH,
                         border_radius=Style.BUTTON_BORDER_RADIUS)
        text_surf = self.font.render(self.text if len(self.text) else self.placeholder, self.font_size)
        r = text_surf.get_rect(centery=self.rect.centery, x=self.rect.x + Style.PADDING)
        if not self.dynamic_width and r.width > self.rect.width - Style.PADDING * 2:
            text_surf = utils.clip(text_surf, pygame.Rect(r.width - self.width, 0, self.width, r.height))
            r = text_surf.get_rect(centery=r.centery, right=self.rect.right-Style.PADDING)

        surf.blit(text_surf, r)
        if self.selected:
            pygame.draw.line(surf, Style.FONT_COLOR, (r.x + self.cursor_pixel_pos, r.y),
                             (r.x + self.cursor_pixel_pos, r.bottom), width=int(self.font_size))

    def _process_key(self, key, unicode):
        nm = f"_process_{pygame.key.name(key)}"
        self.pressed[key] = (unicode, 0)
        if hasattr(self, nm):
            getattr(self, nm)()
        else:
            self._process_other(unicode)

    def update(self, events, dt):
        if not self.selected:
            return
        for e in events:
            if e.type == pygame.KEYDOWN:
                self._process_key(e.key, e.unicode)
            elif e.type == pygame.KEYUP:
                del self.pressed[e.key]
        for k, d in self.pressed.items():
            u, t = d
            if t > self.repeat_delay + self.repeat_timeout:
                self._process_key(k, u)
                self.pressed[k] = (u, self.repeat_timeout)
            else:
                self.pressed[k] = (u, t + dt)

    def _process_delete(self):
        self.right = self.right[1:]

    def _process_backspace(self):
        self.left = self.left[:-1]

    # def _process_right(self):
    #     self.cursor_pos += 1
    #
    # def _process_left(self):
    #     self.cursor_pos -= 1

    def _process_end(self):
        self.cursor_pos = len(self.text)

    def _process_home(self):
        self.cursor_pos = 0

    def _process_return(self):
        return

    def _process_other(self, unicode):
        if unicode in self.font.chars.keys() or unicode == " ":
            self.left += unicode
