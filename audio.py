import pygame
import os

# Initialize mixer with optimized settings
pygame.mixer.pre_init(44100, -16, 2, 512)  # Low-latency, good quality
pygame.mixer.init()

# Define base path for assets
BASE_PATH = os.path.dirname(__file__)  # Gets the directory of audio.py
SOUNDS_PATH = os.path.join(BASE_PATH, "assets", "sounds")

# Load sounds
SOUNDS = {
    "lazer_shot": pygame.mixer.Sound("assets/sounds/lazer.wav"),
    "pig_squeal": pygame.mixer.Sound("assets/sounds/pig_squeal.wav"),
    "pigs_grazing": pygame.mixer.Sound("assets/sounds/pigs_grazing.wav"),
    "game_over": pygame.mixer.Sound("assets/sounds/game_over.wav")
}

# Adjust volumes (normalize sound levels)
SOUNDS["lazer_shot"].set_volume(1)
SOUNDS["pig_squeal"].set_volume(0.1)
SOUNDS["pigs_grazing"].set_volume(0.7)
SOUNDS["game_over"].set_volume(1)


# Function to play a sound
def play_sound(sound_file, loop=False):
    sound = pygame.mixer.Sound(f"assets/sounds/{sound_file}.wav")
    sound.play(loops=-1 if loop else 0)  # Loop if specified
    return sound  # ✅ Return the sound object
