import pygame
import random
from boar import Boar
from constants import *


class PigPen(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-BOAR_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + BOAR_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -BOAR_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + BOAR_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        # ✅ Default to empty tuple if not set
        super().__init__(getattr(self, "containers", ()))
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        boar = Boar(position.x, position.y, radius)
        boar.velocity = velocity

        # ✅ Ensure boar is added to all required sprite groups
        for group in Boar.containers:
            group.add(boar)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > BOAR_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new boar at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, BOAR_KINDS)
            self.spawn(BOAR_MIN_RADIUS * kind, position, velocity)
