import pygame
from audio import play_sound

# Base class for game objects


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # ✅ Default to empty tuple if not set
        super().__init__(getattr(self, "containers", ()))

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        self.rect.center = self.position  # ✅ Keep rect centered on position

    def collides_with(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius
