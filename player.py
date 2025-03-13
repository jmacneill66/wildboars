import pygame
import math
from constants import *
from circleshape import CircleShape
from shot import Shot
from audio import *


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.rev_image = False
        self.toggle_timer = 0  # Cooldown for toggling images

        # ✅ Load images
        self.original_image = pygame.image.load(
            "assets/images/player.png").convert_alpha()
        self.rev_original_image = pygame.image.load(
            "assets/images/player_rev.png").convert_alpha()

        self.active_image = self.original_image  # Active image reference
        self.image = self.active_image  # Current displayed image
        self.rect = self.image.get_rect(
            center=self.position)  # ✅ Set initial position

        # ✅ Mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

    # Countdown and Game Over screen variables
        self.countdown_time = 3
        self.game_over = False
        self.countdown_font = pygame.font.Font(None, 150)
        self.game_over_font = pygame.font.Font(None, 150)
        self.countdown_alpha = 255
        self.countdown_color = (255, 255, 255)

    def draw(self, screen):
        """ Draw the rotated player image on the screen """
        screen.blit(self.image, self.rect.topleft)

        # Draw countdown if active
        if self.countdown_time > 0:
            self.draw_countdown(screen)

        # Draw Game Over screen if triggered
        if self.game_over:
            self.draw_game_over(screen)

    def draw_countdown(self, screen):
        """ Draw countdown in the center of the screen """
        text = self.countdown_font.render(
            str(self.countdown_time), True, self.countdown_color)
        text.set_alpha(self.countdown_alpha)
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(
            40, 40))  # Background box
        screen.blit(text, text_rect)
        self.countdown(screen)

    def draw_game_over(self, screen):
        """ Display Game Over screen """
        text = self.game_over_font.render("GAME OVER!", True, (255, 0, 0))
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(
            50, 50))  # Background box
        screen.blit(text, text_rect)

    def update(self, dt):
        """ Update player state """
        self.shoot_timer -= dt
        self.toggle_timer -= dt  # Reduce toggle cooldown
        mouse_buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        # Countdown logic
        if self.countdown_time > 0:
            self.countdown_alpha -= 5  # Fade effect
            if self.countdown_alpha <= 0:
                self.countdown_alpha = 255
                self.countdown_time -= 1
                self.countdown_color = (
                    255, 0, 0) if self.countdown_time % 2 == 0 else (255, 255, 255)

            return  # Prevent movement during countdown

        # 🎯 Instantly Enable Mouse Control After Countdown
        self.position = pygame.Vector2(pygame.mouse.get_pos())
        self.rect.center = self.position  # Ensure hitbox follows the position

        # 🏃 Movement and Rotation
        if keys[pygame.K_w]:
            self.move(dt * 5)
        if keys[pygame.K_s]:
            self.move(-dt * 5)
        if keys[pygame.K_a]:
            self.rotate(-dt * 100)  # Rotate Left
        if keys[pygame.K_d]:
            self.rotate(dt * 100)  # Rotate Right

        # 🔫 Shooting
        if keys[pygame.K_SPACE] or mouse_buttons[0]:  # Space or Left-click
            play_sound("lazer_shot")
            self.shoot()

        # 🔄 Toggle Image with 'R' Key or Right-click
        if (keys[pygame.K_r] or mouse_buttons[2]) and self.toggle_timer <= 0:  # Right-click or 'R' key
            self.rev_image = not self.rev_image  # Toggle boolean value
            self.active_image = self.rev_original_image if self.rev_image else self.original_image
            self.toggle_timer = 0.2  # Cooldown to prevent rapid toggling
            self.rotate(0)  # Reapply rotation to new image

    def rotate(self, angle):
        """ Rotate the player by a given angle """
        self.rotation += angle
        self.image = pygame.transform.rotate(self.active_image, -self.rotation)
        self.rect = self.image.get_rect(
            center=self.rect.center)  # Keep center position

    def move(self, dt):
        """ Move the player forward in the direction it is facing """
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.rect.center = self.position  # Keep rect in sync

    def shoot(self):
        """ Fire a shot in the direction the player is facing """
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

        # 🎯 Adjust shot spawn position based on current image
        # Adjusted to 10 and 2 o'clock angles
        angle_offset = 340 if self.rev_image else 200
        offset_distance = self.radius * 1.16

        radian_angle = math.radians(self.rotation + angle_offset)
        offset_x = offset_distance * math.cos(radian_angle)
        offset_y = offset_distance * math.sin(radian_angle)

        shot_x = self.position.x + offset_x
        shot_y = self.position.y + offset_y

        # 🔫 Create shot and apply velocity
        shot = Shot(shot_x, shot_y, self.rotation)
        shot.velocity = pygame.Vector2(
            math.cos(radian_angle), math.sin(radian_angle)) * PLAYER_SHOOT_SPEED

        # ✅ Add shot to sprite groups
        for group in Shot.containers:
            group.add(shot)

    def countdown(self, screen):
        font = pygame.font.Font(None, 100)  # Define font inside function

        for i in range(3, 0, -1):  # Countdown from 3 to 1
            screen.fill((0, 70, 0))  # Clear screen, dark green

            # Draw countdown frame
            # (x, y, width, height)
            frame_rect = pygame.Rect(700, 350, 400, 200)
            # Dark gray background
            pygame.draw.rect(screen, (0, 50, 0), frame_rect)
            pygame.draw.rect(screen, (255, 255, 0),
                             frame_rect, 5)  # Yellow border

            # Render countdown text
            text_surface = self.countdown_font.render(
                str(i), True, (255, 255, 0))  # Yellow text
            text_rect = text_surface.get_rect(center=frame_rect.center)
            screen.blit(text_surface, text_rect)

            pygame.display.flip()  # Update display
            pygame.time.delay(1000)  # Wait 1 second before next number

    def trigger_game_over(self, screen):
        """ Trigger game over screen """
        if self.game_over:  # Prevent multiple calls
            return
        self.game_over = True
        screen.fill((0, 0, 0))  # Black background
        # Draw Game Over frame
        frame_rect = pygame.Rect(500, 350, 800, 200)
        # Dark gray background
        pygame.draw.rect(screen, (50, 50, 50), frame_rect)
        pygame.draw.rect(screen, (255, 0, 0), frame_rect, 5)  # Red border

        # Render Game Over text
        text_surface = self.game_over_font.render(
            "GAME OVER!", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=frame_rect.center)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        play_sound("game_over", loop=False)
        pygame.time.delay(3000)  # Show Game Over screen for 3 seconds
