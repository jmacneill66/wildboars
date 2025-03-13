import pygame
import random
from constants import *
from circleshape import CircleShape
from player import *
from baconbit import *


class Boar(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

       # Determine size based on the radius
        if radius == BOAR_MIN_RADIUS:
            self.size = "small"
        elif radius == BOAR_MID_RADIUS:
            self.size = "medium"
        elif radius == BOAR_MAX_RADIUS:
            self.size = "large"
        else:
            raise ValueError(f"Invalid boar size: {radius}")

        # Load the image based on size
        self.image = pygame.image.load(
            f"assets/images/boar_{self.size}.png").convert_alpha()

        # Set the image's rect
        self.rect = self.image.get_rect(center=(x, y))

        # ✅ Create pixel-perfect collision mask
        self.mask = pygame.mask.from_surface(self.image)

    def collides_with(self, sprite):
        # Pixel-perfect collision
        if self.mask.overlap(sprite.mask, (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)):
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = (self.position.x, self.position.y)

    def split(self):
        """Split into two smaller boars if not already the smallest"""
        self.kill()
        from score import Player_Score  # ✅ Ensure latest reference

        # ✅ Spawn bacon bits when splitting
        for _ in range(20):  # Adjust number of # 🍖 bacon bits
            bacon_bit = BaconBit(
                self.position.x, self.position.y, (235, 235, 235))

            for group in BaconBit.containers:
                group.add(bacon_bit)

        # If boar is too small, don't split
        if self.radius <= BOAR_MIN_RADIUS:
            Player_Score.add_points(30)
            return

        random_angle = random.uniform(20, 50)
        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        # Determine new radius for split boars
        if self.size == "large":
            Player_Score.add_points(10)
            new_radius = BOAR_MID_RADIUS
        elif self.size == "medium":
            Player_Score.add_points(20)
            new_radius = BOAR_MIN_RADIUS
        else:
            return  # Small boars don't split

        # ✅ Create new boars and add them to all sprite groups
        new_boar_1 = Boar(self.position.x, self.position.y, new_radius)
        new_boar_1.velocity = a
        for group in self.containers:
            group.add(new_boar_1)

        new_boar_2 = Boar(self.position.x, self.position.y, new_radius)
        new_boar_2.velocity = b
        for group in self.containers:
            group.add(new_boar_2)
