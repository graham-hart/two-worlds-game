import os

import pygame


def load(path):
    img = pygame.image.load(path)
    return img if pygame.display.get_surface() is None else img.convert_alpha()


def load_dir(path):
    imgs = {}
    for file in os.listdir(path):
        if not os.path.isdir(file) and file.endswith(".png") or file.endswith(".jpg"):
            imgs[os.path.splitext(file)[0]] = load(os.path.join(path, file))
    return imgs
