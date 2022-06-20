import json
import os

from engine import utils
from engine.graphics import image


class AnimData:
    def __init__(self, path):
        config = json.load(open(os.path.join(path, "config.json")))
        self.frame_delays = config["frame-delays"]
        self.repeat = config["repeat"]
        self.outline = config["outline"]
        self.speed = config["speed"]
        imgs = image.load_dir(path)
        self.images = [imgs[k] for k in sorted(imgs.keys())]


class Animation:
    def __init__(self, data: AnimData):
        self.data = data
        self.paused = False
        self.current_frame = 0
        self.since_advance = 0

    def image(self):
        img = self.data.images[self.current_frame]
        if not self.data.outline:
            return img

        outline = utils.outline(img)
        outline.blit(img, (1, 1))
        return outline

    def advance(self):
        self.since_advance = 0
        if self.current_frame == len(self.data.images) - 1:
            if self.data.repeat:
                self.current_frame = 0
                return
        else:
            self.current_frame += 1

    def update(self):
        self.since_advance += 1
        if self.since_advance >= self.data.frame_delays[self.current_frame] / self.data.speed:
            self.advance()


class AnimManager:
    anim_data = {}

    @classmethod
    def load(cls, animations_path):
        cls.anim_data = {}
        for file in os.listdir(animations_path):
            if not os.path.isdir(file):
                cls.anim_data[file] = AnimData(os.path.join(animations_path, file))

    @classmethod
    def new_anim(cls, anim):
        return Animation(cls.anim_data[anim])
