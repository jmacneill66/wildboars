import pygame
import time
import sys
from constants import *
from player import *
from boar import Boar
from pigpen import PigPen
from shot import Shot
from baconbit import BaconBit
from audio import *
from score import init_score


def main():
    pygame.init()
    pygame.mixer.init()
    init_score()
    from score import Player_Score
    pygame.font.init()  # Ensure fonts are initialized
    pygame.display.set_caption("Wild Boars Game")  # 🏆 Set custom window title
    background_sound = play_sound(
        "pigs_grazing", loop=True)  # Store background sound
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Initialize all sprite groups and containers here
    bacon_bits = pygame.sprite.Group()
    boars = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    Boar.containers = (boars, updateable, drawable)
    PigPen.containers = updateable
    Shot.containers = (shots, updateable, drawable)
    BaconBit.containers = (bacon_bits, updateable, drawable)

    pigpen = PigPen()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player.draw(screen)
    screen.fill((0, 0, 0))  # Clear screen after countdown
    pygame.display.flip()
    running = True
    game_over = False
    game_over_triggered = False  # ✅ Prevents sound spamming on game end

    dt = 0
    game_over_timer = 0  # ⏳ Track delay before quitting
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:  # Scroll Up
                    player.rotate(dt*200)  # Rotate Right
                elif event.y < 0:  # Scroll Down
                    player.rotate(-dt*200)  # Rotate Left

        if not game_over:  # Only update objects if the game isn't over
            updateable.update(dt)
            # ✅ Draw sprites

        if game_over and not game_over_triggered:
            game_over_triggered = True  # Prevent background audio looping
            game_over_timer = time.time() + 1  # Set 1-second delay from current time

        if game_over and game_over_timer <= time.time():
            running = False  # Quit game
            pygame.quit()  # Properly quit Pygame
            sys.exit()  # Ensure the script exits cleanly

        for boar in boars:
            if boar.collides_with(player):
                background_sound.stop()
                game_over = True  # Freeze movement
                player.trigger_game_over(screen)

            for shot in shots:
                if boar.collides_with(shot):
                    play_sound("pig_squeal", loop=False)
                    shot.kill()
                    boar.split()

        # ✅ Rendering
        screen.fill((0, 90, 0))  # Dark green background
        drawable.draw(screen)  # ✅ Draws normal sprites
        bacon_bits.update(dt)  # Update bacon bits
        bacon_bits.draw(screen)
        Player_Score.draw(screen)  # ✅ Safe to use
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Maintain 60 FPS


if __name__ == "__main__":
    main()
