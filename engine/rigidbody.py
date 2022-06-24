import pygame
from engine.state import Game

class RigidBody:
    GRAVITY = 1

    def __init__(self, entity):
        self.entity = entity
        self.movement = pygame.Vector2(0)
        self.velocity = pygame.Vector2(0)
        self.acceleration = pygame.Vector2(0)

    def update(self, tilemap):
        self.velocity.y += RigidBody.GRAVITY * Game.dt
        self._move(tilemap, self.movement+self.velocity)
        self.movement = pygame.Vector2(0)

    def add_vel(self, vel: pygame.Vector2):
        self.velocity += vel

    def collision_list(self, tiles):
        return [t for t in tiles if t.rect.colliderect(self.entity.rect)]

    def move(self, amount: pygame.Vector2):
        self.movement += amount

    def _move(self, tilemap, amount:pygame.Vector2):
        all_collisions = []
        tiles = tilemap.tiles()
        normal_tiles = [t for t in tiles if t.ramp == 0]
        ramps = [t for t in tiles if t.ramp != 0]

        # Test x movement
        self.entity.pos = pygame.Vector2(amount.x+self.entity.pos.x, self.entity.pos.y)
        collisions = self.collision_list(normal_tiles)
        all_collisions += collisions
        for tile in collisions:
            if tile.rect.x < self.entity.rect.x:
                self.entity.rect.left = tile.rect.right
            else:
                self.entity.rect.right = tile.rect.left

        self.entity.pos = pygame.Vector2(self.entity.pos.x, self.entity.pos.y+amount.y)
        collisions = self.collision_list(normal_tiles)
        all_collisions += collisions
        for tile in collisions:
            if tile.rect.y < self.entity.rect.y:
                self.entity.rect.top = tile.rect.bottom
            else:
                self.entity.rect.bottom = tile.rect.top
                self.velocity.y = self.velocity.y if self.velocity.y < 0 else 0
