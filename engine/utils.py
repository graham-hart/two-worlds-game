import pygame

def floor_to_interval(val, interval):
    return val // interval * interval


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


def outline(surf: pygame.Surface, border=True, color=(255, 255, 255)):
    outline_surf = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
    mask = pygame.mask.from_surface(surf)
    for pt in mask.outline():
        outline_surf.set_at(pt, color)
    outline_surf.set_colorkey((0, 0, 0))
    if not border:
        return outline_surf
    border_surf = pygame.Surface(pygame.Vector2(2) + pygame.Vector2(surf.get_size()), flags=pygame.SRCALPHA)
    border_surf.blit(outline_surf, (1, 0))  # Top
    border_surf.blit(outline_surf, (0, 1))  # Left
    border_surf.blit(outline_surf, (2, 1))  # Bottom
    border_surf.blit(outline_surf, (1, 2))  # Right
    return border_surf


def stretch_img_center_horiz(img: pygame.Surface, center_min, center_max, new_width):
    left_cap = clip(img, pygame.Rect(0, 0, center_min, img.get_height()))
    right_cap = clip(img, pygame.Rect(center_max + 1, 0, img.get_width() - center_max - 1, img.get_height()))
    center_img = pygame.transform.scale(
        clip(img, pygame.Rect(center_min, 0, center_max - center_min + 1, img.get_height())),
        (new_width - center_min - (img.get_width() - center_max) + 1, img.get_height()))
    new_surf = pygame.Surface((new_width, img.get_height()), flags=pygame.SRCALPHA)
    new_surf.blit(center_img, (center_min, 0))
    new_surf.blit(left_cap, (0, 0))
    new_surf.blit(right_cap, (new_width - right_cap.get_width(), 0))
    new_surf.set_colorkey((0, 0, 0))
    return new_surf
