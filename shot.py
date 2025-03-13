import pygame
from constants import *
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)

        # ✅ Create an image for Shot (yellow circle)
        self.image = pygame.Surface(
            (SHOT_RADIUS * 2, SHOT_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0),
                           (SHOT_RADIUS, SHOT_RADIUS), SHOT_RADIUS)

        # ✅ Rotate image to match shot direction
        self.image = pygame.Surface(
            (SHOT_RADIUS * 2, SHOT_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0),
                           (SHOT_RADIUS, SHOT_RADIUS), SHOT_RADIUS)

        # Create mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)

        # ✅ Set position
        self.rect = self.image.get_rect(center=(x, y))

        # ✅ Set velocity based on angle
        self.velocity = velocity

    def collides_with(self, sprite):
        # Pixel-perfect collision
        return self.mask.overlap(sprite.mask, (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y))

    def update(self, dt):
        """ Move the shot """
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
