"""
Configuration settings and constants for the game.
"""
import os
import pygame

# Initialize pygame
pygame.init()

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
AUDIO_DIR = os.path.join(ROOT_DIR, "audio_files")

# Display settings
WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realms of Fate: Chronicles Unbound")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
DARK_RED = (139, 0, 0, 220)  # Added transparency
DARKER_RED = (100, 0, 0, 200)  # For button shadow with transparency
LIGHT_RED = (178, 34, 34, 220)  # For hover effect with transparency
VERY_DARK_PURPLE = (40, 0, 40)  # For title frame

# Fonts
try:
    TITLE_FONT = pygame.font.Font(os.path.join(ASSETS_DIR, "medieval.ttf"), 80)
    SUBTITLE_FONT = pygame.font.Font(os.path.join(ASSETS_DIR, "medieval.ttf"), 40)
    MENU_FONT = pygame.font.Font(os.path.join(ASSETS_DIR, "medieval.ttf"), 45)
except:
    print("Warning: Could not load custom fonts, using system fonts")
    TITLE_FONT = pygame.font.SysFont("serif", 80)
    SUBTITLE_FONT = pygame.font.SysFont("serif", 40)
    MENU_FONT = pygame.font.SysFont("serif", 45)

# Asset loading helper functions
def load_image(filename, size=None):
    """Load an image and resize it if needed."""
    try:
        path = os.path.join(ASSETS_DIR, filename)
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except:
        print(f"Warning: Could not load image {filename}")
        return None

def load_sound(filename):
    """Load a sound effect."""
    try:
        path = os.path.join(AUDIO_DIR, filename)
        return pygame.mixer.Sound(path)
    except:
        print(f"Warning: Could not load sound {filename}")
        return None

# Load common assets
BACKGROUND_IMG = load_image("fantasy_background.jpg", (WIDTH, HEIGHT))
CURSOR_IMG = load_image("fantasy_cursor.png", (32, 32))
BUTTON_SOUND = load_sound("menu_button.mp3")

# Try to load and play background music
try:
    pygame.mixer.music.load(os.path.join(AUDIO_DIR, "background_music.mp3"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except:
    print("Warning: Could not load background music")