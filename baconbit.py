import random
import pygame


class BaconBit(pygame.sprite.Sprite):
    def __init__(self, x, y, color, lifetime=0.25):
        super().__init__(self.containers)  # ✅ Automatically add to container

        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        self.image.fill(color)  # Set color
        self.rect = self.image.get_rect(center=(x, y))

        self.velocity = pygame.Vector2(
            random.uniform(-2, 2), random.uniform(-2, 2)
        ) * 3

        self.lifetime = lifetime  # Seconds
        self.spawn_time = pygame.time.get_ticks() / 1000

    def update(self, dt):
        """Move and fade out particles over time"""
        self.rect.x += self.velocity.x * dt * 30
        self.rect.y += self.velocity.y * dt * 30

        elapsed = (pygame.time.get_ticks() / 1000) - self.spawn_time
        if elapsed > self.lifetime:
            self.kill()
