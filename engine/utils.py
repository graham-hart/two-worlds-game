import pygame


def clip(surf: pygame.Surface, rect: pygame.Rect):
    return surf.subsurface(rect).copy()


def filled_surf(color, size):
    s = pygame.Surface((1, 1))
    s.set_at((0, 0), color)
    return pygame.transform.scale(s, size)


def color_swap(image: pygame.Surface, old_color, new_color):
    cp = pygame.Surface(image.get_size())
    cp.fill(new_color)
    image.set_colorkey(old_color)
    cp.blit(image, (0, 0))
    return cp


def clamp(val, mn, mx):
    return min(max(val, mn), mx)


def outline(surf: pygame.Surface, border=True):
    outline_surf = pygame.Surface(surf.get_size())
    mask = pygame.mask.from_surface(surf)
    for pt in mask.outline():
        outline_surf.set_at(pt, (255, 255, 255))
    outline_surf.set_colorkey((0, 0, 0))
    if not border:
        return outline_surf
    border_surf = pygame.Surface(pygame.Vector2(2) + pygame.Vector2(surf.get_size()))
    border_surf.blit(outline_surf, (1, 0))  # Top
    border_surf.blit(outline_surf, (0, 1))  # Left
    border_surf.blit(outline_surf, (2, 1))  # Bottom
    border_surf.blit(outline_surf, (1, 2))  # Right
    return border_surf
