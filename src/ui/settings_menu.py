"""
Settings menu for the game.
"""
import math
import pygame
import sys
import os

# Add the root directory to the path so we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import (
    WIDTH, HEIGHT, GOLD, DARK_GOLD, VERY_DARK_PURPLE, 
    DARK_RED, LIGHT_RED, SCREEN, BACKGROUND_IMG,
    CURSOR_IMG, TITLE_FONT, SUBTITLE_FONT, MENU_FONT
)
from src.ui.button import Button
from src.ui.effects import draw_decorative_frame, create_ambient_particles, update_ambient_particles

class SettingsMenu:
    """Settings menu screen."""
    
    def __init__(self):
        # Create a semi-transparent overlay for better text readability
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))  # Black with 60% opacity
        
        # Create decorative title frame
        self.title_frame = pygame.Rect(WIDTH//2 - 400, HEIGHT//6 - 50, 800, 100)
        
        # Create settings panel frame
        self.settings_frame = pygame.Rect(WIDTH//2 - 450, HEIGHT//4, 900, 500)
        
        # Create buttons
        button_width, button_height = 400, 75
        button_x = WIDTH//2 - button_width//2
        
        # Back button
        self.buttons = {
            'back': Button("Back to Main Menu", (button_x, HEIGHT - 150), 
                          (button_width, button_height), DARK_RED, LIGHT_RED)
        }
        
        # Settings labels (position and text)
        self.settings_labels = {
            'music': {"text": "Music Volume", "pos": (WIDTH//2 - 350, HEIGHT//4 + 80 + button_height//2)},
            'sfx': {"text": "Sound Effects", "pos": (WIDTH//2 - 350, HEIGHT//4 + 180 + button_height//2)},
            'fullscreen': {"text": "Fullscreen", "pos": (WIDTH//2 - 350, HEIGHT//4 + 280 + button_height//2)},
            'difficulty': {"text": "Difficulty", "pos": (WIDTH//2 - 350, HEIGHT//4 + 380 + button_height//2)}
        }
        
        # Settings values and states
        self.settings = {
            'music_volume': 0.4,  # 0.0 to 1.0
            'sfx_volume': 1.0,    # 0.0 to 1.0
            'fullscreen': False,
            'difficulty': 1       # 0: Easy, 1: Normal, 2: Hard
        }
        
        # Slider regions
        self.slider_regions = {
            'music': pygame.Rect(WIDTH//2 + 50, HEIGHT//4 + 80 + button_height//2 - 10, 300, 20),
            'sfx': pygame.Rect(WIDTH//2 + 50, HEIGHT//4 + 180 + button_height//2 - 10, 300, 20)
        }
        
        # Toggle/selection regions
        self.toggle_regions = {
            'fullscreen': pygame.Rect(WIDTH//2 + 50, HEIGHT//4 + 280 + button_height//2 - 15, 30, 30),
            'difficulty': [
                pygame.Rect(WIDTH//2 + 50, HEIGHT//4 + 380 + button_height//2 - 15, 80, 30),  # Easy
                pygame.Rect(WIDTH//2 + 150, HEIGHT//4 + 380 + button_height//2 - 15, 80, 30), # Normal
                pygame.Rect(WIDTH//2 + 250, HEIGHT//4 + 380 + button_height//2 - 15, 80, 30)  # Hard
            ]
        }
        
        # Active slider (if user is dragging)
        self.active_slider = None
        
        # Dragging state
        self.is_dragging = False
        
        # For background animation
        self.bg_offset = 0
        
        # Create ambient particles
        self.ambient_particles = create_ambient_particles()
        
        # Create a clock to control frame rate
        self.clock = pygame.time.Clock()
        
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Check main button events
            if self.buttons['back'].handle_event(event):
                self.save_settings()
                return "main_menu"
                
            # Handle mouse events for sliders and toggles
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check sliders
                for setting, rect in self.slider_regions.items():
                    if rect.collidepoint(mouse_pos):
                        self.active_slider = setting
                        self.is_dragging = True
                        # Update value based on click position
                        self.update_slider_value(setting, mouse_pos[0])
                
                # Check toggles
                if self.toggle_regions['fullscreen'].collidepoint(mouse_pos):
                    self.settings['fullscreen'] = not self.settings['fullscreen']
                    self.toggle_fullscreen()
                
                # Check difficulty options
                for i, rect in enumerate(self.toggle_regions['difficulty']):
                    if rect.collidepoint(mouse_pos):
                        self.settings['difficulty'] = i
            
            # Handle slider dragging
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_dragging = False
                self.active_slider = None
            
            elif event.type == pygame.MOUSEMOTION and self.is_dragging and self.active_slider:
                self.update_slider_value(self.active_slider, event.pos[0])
                
        return None  # No state change
    
    def update_slider_value(self, setting, x_pos):
        """Update slider value based on mouse position."""
        slider_rect = self.slider_regions[setting]
        # Calculate relative position (0.0 to 1.0)
        rel_pos = max(0.0, min(1.0, (x_pos - slider_rect.left) / slider_rect.width))
        
        # Update the appropriate setting
        if setting == 'music':
            self.settings['music_volume'] = rel_pos
            # Actually update the game's music volume
            pygame.mixer.music.set_volume(rel_pos)
        elif setting == 'sfx':
            self.settings['sfx_volume'] = rel_pos
            # Update the button sound volume
            from config import BUTTON_SOUND
            if BUTTON_SOUND:
                BUTTON_SOUND.set_volume(rel_pos)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.settings['fullscreen']:
            # Switch to fullscreen
            pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            # Switch to windowed
            pygame.display.set_mode((WIDTH, HEIGHT))
    
    def save_settings(self):
        """Save settings to a configuration file."""
        # In a real implementation, you'd save to a file
        print("Saving settings:")
        for setting, value in self.settings.items():
            print(f"  {setting}: {value}")
    
    def update(self):
        """Update menu state."""
        time_passed = self.clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button states
        for button in self.buttons.values():
            button.update(mouse_pos, time_passed)
            
        # Update background offset for animation
        self.bg_offset = (self.bg_offset + 0.1) % WIDTH
        
        return time_passed
    
    def draw(self):
        """Draw the settings screen."""
        # Draw background
        if BACKGROUND_IMG:
            # Create a subtle moving background effect
            SCREEN.blit(BACKGROUND_IMG, (-self.bg_offset, 0))
            SCREEN.blit(BACKGROUND_IMG, (WIDTH - self.bg_offset, 0))
        else:
            # If no background image, use a gradient
            for y in range(HEIGHT):
                # Create a dark gradient
                color_value = max(0, min(50, 50 - (y / HEIGHT) * 50))
                pygame.draw.line(SCREEN, (color_value, color_value, color_value * 0.8), 
                               (0, y), (WIDTH, y))
        
        # Apply the semi-transparent overlay
        SCREEN.blit(self.overlay, (0, 0))
        
        # Update and draw ambient particles
        update_ambient_particles(self.ambient_particles)
        
        # Draw title frame
        dark_frame_surface = pygame.Surface((self.title_frame.width, self.title_frame.height), pygame.SRCALPHA)
        dark_frame_surface.fill((VERY_DARK_PURPLE[0], VERY_DARK_PURPLE[1], VERY_DARK_PURPLE[2], 180))
        SCREEN.blit(dark_frame_surface, (self.title_frame.x, self.title_frame.y))
        draw_decorative_frame(SCREEN, self.title_frame, GOLD, width=3, fancy=True)
        
        # Draw settings frame
        settings_frame_surface = pygame.Surface((self.settings_frame.width, self.settings_frame.height), pygame.SRCALPHA)
        settings_frame_surface.fill((VERY_DARK_PURPLE[0], VERY_DARK_PURPLE[1], VERY_DARK_PURPLE[2], 160))
        SCREEN.blit(settings_frame_surface, (self.settings_frame.x, self.settings_frame.y))
        draw_decorative_frame(SCREEN, self.settings_frame, GOLD, width=3, fancy=True)
        
        # Draw title with shadow effect
        shadow_offsets = [(3, 3), (2, 2)]
        for offset in shadow_offsets:
            shadow_text = TITLE_FONT.render("Settings", True, DARK_GOLD)
            shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + offset[0], HEIGHT//6 + offset[1]))
            SCREEN.blit(shadow_text, shadow_rect)
            
        title_text = TITLE_FONT.render("Settings", True, GOLD)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//6))
        SCREEN.blit(title_text, title_rect)
        
        # Draw settings labels with engraved effect
        self.draw_engraved_labels()
        
        # Draw sliders
        self.draw_sliders()
        
        # Draw toggles and selections
        self.draw_toggles()
        
        # Draw back button
        self.buttons['back'].draw(SCREEN)
        
        # Draw a custom cursor instead of the default one
        if CURSOR_IMG:
            cursor_rect = CURSOR_IMG.get_rect(center=pygame.mouse.get_pos())
            SCREEN.blit(CURSOR_IMG, cursor_rect)
        
        # Update the display
        pygame.display.flip()
    
    def draw_sliders(self):
        """Draw slider controls."""
        # Music volume slider
        self.draw_slider(
            self.slider_regions['music'], 
            self.settings['music_volume'], 
            f"{int(self.settings['music_volume'] * 100)}%"
        )
        
        # SFX volume slider
        self.draw_slider(
            self.slider_regions['sfx'], 
            self.settings['sfx_volume'],
            f"{int(self.settings['sfx_volume'] * 100)}%"
        )
    
    def draw_slider(self, rect, value, label):
        """Draw an individual slider with given value."""
        # Draw slider background
        pygame.draw.rect(SCREEN, DARK_GOLD, rect, border_radius=5)
        
        # Draw slider fill
        fill_rect = pygame.Rect(rect.left, rect.top, rect.width * value, rect.height)
        pygame.draw.rect(SCREEN, GOLD, fill_rect, border_radius=5)
        
        # Draw slider knob
        knob_pos = (rect.left + rect.width * value, rect.centery)
        pygame.draw.circle(SCREEN, DARK_RED, knob_pos, 15)
        pygame.draw.circle(SCREEN, LIGHT_RED, knob_pos, 13)
        pygame.draw.circle(SCREEN, GOLD, knob_pos, 5)
        
        # Draw label
        label_font = pygame.font.SysFont("serif", 24)
        label_text = label_font.render(label, True, GOLD)
        label_rect = label_text.get_rect(midright=(rect.right + 80, rect.centery))
        SCREEN.blit(label_text, label_rect)
    
    def draw_engraved_labels(self):
        """Draw setting labels with an engraved effect."""
        for setting, label_info in self.settings_labels.items():
            # First draw the darker "shadow" text slightly offset
            shadow_text = MENU_FONT.render(label_info["text"], True, DARK_GOLD)
            shadow_rect = shadow_text.get_rect(midleft=(label_info["pos"][0], label_info["pos"][1] + 2))
            SCREEN.blit(shadow_text, shadow_rect)
            
            # Then draw the main text slightly above to create engraved effect
            main_text = MENU_FONT.render(label_info["text"], True, GOLD)
            main_rect = main_text.get_rect(midleft=(label_info["pos"][0], label_info["pos"][1]))
            SCREEN.blit(main_text, main_rect)
            
    def draw_toggles(self):
        """Draw toggle and selection controls."""
        # Fullscreen toggle
        toggle_rect = self.toggle_regions['fullscreen']
        pygame.draw.rect(SCREEN, DARK_GOLD, toggle_rect, border_radius=5)
        
        if self.settings['fullscreen']:
            # Filled when enabled
            pygame.draw.rect(SCREEN, GOLD, pygame.Rect(toggle_rect.left + 3, toggle_rect.top + 3, 
                                                    toggle_rect.width - 6, toggle_rect.height - 6), 
                           border_radius=3)
        
        # Label for fullscreen
        toggle_label = "On" if self.settings['fullscreen'] else "Off"
        label_font = pygame.font.SysFont("serif", 24)
        label_text = label_font.render(toggle_label, True, GOLD)
        label_rect = label_text.get_rect(midleft=(toggle_rect.right + 20, toggle_rect.centery))
        SCREEN.blit(label_text, label_rect)
        
        # Difficulty selection
        difficulty_labels = ["Easy", "Normal", "Hard"]
        for i, rect in enumerate(self.toggle_regions['difficulty']):
            # Draw rectangle for each option
            color = GOLD if i == self.settings['difficulty'] else DARK_GOLD
            pygame.draw.rect(SCREEN, color, rect, border_radius=5)
            
            # Draw label
            diff_text = label_font.render(difficulty_labels[i], True, VERY_DARK_PURPLE)
            diff_rect = diff_text.get_rect(center=rect.center)
            SCREEN.blit(diff_text, diff_rect)
    
    def run(self):
        """Run the settings menu loop."""
        while True:
            # Handle events
            state_change = self.handle_events()
            if state_change:
                return state_change
            
            # Update
            self.update()
            
            # Draw
            self.draw()