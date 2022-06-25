import pygame
from engine.state import Game
from engine.tile import Tile
from engine import utils
class RigidBody:
    GRAVITY = 1
    FRICTION = 0.7
    def __init__(self, entity):
        self.entity = entity
        self.movement = pygame.Vector2(0)
        self.velocity = pygame.Vector2(0)
        self.acceleration = pygame.Vector2(0)

    def update(self, tilemap):
        self.velocity.y += RigidBody.GRAVITY * Game.dt
        self.velocity.x *= RigidBody.FRICTION
        self._move(tilemap, self.movement+self.velocity)
        self.movement = pygame.Vector2(0)

    def add_vel(self, vel: pygame.Vector2):
        self.velocity += vel

    def collision_list(self, tiles) -> list[Tile]:
        return [t for t in tiles if t.rect.colliderect(self.entity.rect)]

    def move(self, amount: pygame.Vector2):
        self.movement += amount

    def _move(self, tilemap, amount:pygame.Vector2):
        all_collisions = []
        collision_dirs = {d:False for d in ["top", "bottom", "left", "right"]}
        tiles = tilemap.tiles()
        normal_tiles = [t for t in tiles if t.ramp == 0]
        ramp_tiles = [t for t in tiles if t.ramp != 0]

        # Test x movement
        self.entity.pos = pygame.Vector2(amount.x+self.entity.pos.x, self.entity.pos.y)
        collisions = self.collision_list(normal_tiles)
        all_collisions += collisions
        for tile in collisions:
            if tile.rect.x < self.entity.rect.x:
                self.entity.rect.left = tile.rect.right
                collision_dirs["left"] = True
            else:
                self.entity.rect.right = tile.rect.left
                collision_dirs["right"] = True

        # Y movement
        self.entity.pos = pygame.Vector2(self.entity.pos.x, self.entity.pos.y+amount.y)
        collisions = self.collision_list(normal_tiles)
        all_collisions += collisions
        for tile in collisions:
            if tile.rect.y < self.entity.rect.y:
                self.entity.rect.top = tile.rect.bottom
                collision_dirs["top"] = True
            else:
                self.entity.rect.bottom = tile.rect.top
                collision_dirs["bottom"] = True

        # Ramps
        collided_ramps = self.collision_list(ramp_tiles)
        for ramp in collided_ramps:
            ramp_y_pos = 0
            if ramp.ramp == 1:  # Left
                rel_x = self.entity.rect.pos.x - ramp.rect.pos.x
                ramp_y_pos = ramp.rect.height - rel_x
            elif ramp.ramp == 2:  # Left
                rel_x = 1+(self.entity.rect.right - ramp.rect.right)
                ramp_y_pos = rel_x
            ramp_y_pos = utils.clamp(ramp_y_pos, 0, 1)
            y = ramp.rect.y + 1 - ramp_y_pos
            if self.entity.rect.bottom > y:
                self.entity.rect.bottom = y
                all_collisions.append(ramp)
                collision_dirs["bottom"] = True
        self.entity.on_collision(collisions, collision_dirs)
        self.on_collision(collisions, collision_dirs)

    def on_collision(self, collisions, collision_dirs):
        if collision_dirs["bottom"]:
            self.velocity.y = self.velocity.y if self.velocity.y < 0 else 0
        for c in collisions:
            if c.ramp != 0:
                self.velocity *= RigidBody.FRICTION
