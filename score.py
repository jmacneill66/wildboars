import pygame
from constants import *
Player_Score = None  # Define global variable


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y, font_size=40):
        super().__init__()  # ✅ parent class initializes first
        self.score = 0
        self.font = pygame.font.Font(None, 40)  # Default font
        self.color = (255, 255, 40)
        self.position = (x, y)
        self.image = self.font.render(f"SCORE: {self.score}", True, self.color)
        self.rect = self.image.get_rect(topleft=(x, y))  # ✅ Set `rect`

    def add_points(self, points):
        """Increase the score by a given amount"""
        self.score += points
        self.update_image()

    def reset(self):
        """Reset the score to zero."""
        self.score = 0
        self.update_image()

    def draw(self, screen):
        score_text = self.font.render(f"SCORE: {self.score}", True, self.color)
        screen.blit(score_text, self.position)

    def update_image(self):
        """Re-render the score text to update display."""
        self.image = self.font.render(f"SCORE: {self.score}", True, self.color)
        self.rect = self.image.get_rect(
            topleft=self.rect.topleft)  # Keep position


def init_score():
    global Player_Score  # ✅ Ensure global scope is updated
    # ✅ Assign a new Score object
    Player_Score = Score((SCREEN_WIDTH // 2) - 15, SCREEN_HEIGHT - 45)
