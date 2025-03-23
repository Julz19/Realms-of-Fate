"""
Main menu for the game.
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
    CURSOR_IMG, TITLE_FONT, SUBTITLE_FONT
)
from src.ui.button import Button
from src.ui.effects import draw_decorative_frame, create_ambient_particles, update_ambient_particles

class MainMenu:
    """Main menu screen."""
    
    def __init__(self):
        # Create a semi-transparent overlay for better text readability
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))  # Black with 60% opacity
        
        # Create decorative title frame
        self.title_frame = pygame.Rect(WIDTH//2 - 400, HEIGHT//4 - 100, 800, 200)
        
        # Create buttons
        button_width, button_height = 400, 75
        button_x = WIDTH//2 - button_width//2
        
        # Stagger the buttons for visual interest
        self.buttons = {
            'start': Button("New Adventure", (button_x, HEIGHT//2), 
                          (button_width, button_height), DARK_RED, LIGHT_RED),
            
            'load': Button("Load Adventure", (button_x - 20, HEIGHT//2 + 90), 
                         (button_width, button_height), DARK_RED, LIGHT_RED),
            
            'settings': Button("Settings", (button_x + 20, HEIGHT//2 + 180), 
                             (button_width, button_height), DARK_RED, LIGHT_RED),
            
            'exit': Button("Exit", (button_x, HEIGHT//2 + 270), 
                         (button_width, button_height), DARK_RED, LIGHT_RED)
        }
        
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
            
            if self.buttons['start'].handle_event(event):
                print("New Adventure clicked")
                # Here we would transition to character creation or game start
                return "new_game"
            
            if self.buttons['load'].handle_event(event):
                print("Load Adventure clicked")
                # Here we would load saved games
                return "load_game"
            
            if self.buttons['settings'].handle_event(event):
                print("Settings clicked")
                # Here we would show settings menu
                return "settings"
            
            if self.buttons['exit'].handle_event(event):
                pygame.quit()
                sys.exit()
                
        return None  # No state change
    
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
        """Draw the menu screen."""
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
        
        # Draw decorative elements
        # Use darker purple for the title frame
        dark_frame_surface = pygame.Surface((self.title_frame.width, self.title_frame.height), pygame.SRCALPHA)
        dark_frame_surface.fill((VERY_DARK_PURPLE[0], VERY_DARK_PURPLE[1], VERY_DARK_PURPLE[2], 180))
        SCREEN.blit(dark_frame_surface, (self.title_frame.x, self.title_frame.y))
        draw_decorative_frame(SCREEN, self.title_frame, GOLD, width=3, fancy=True)
        
        # Draw main title with better glow effect
        # Multiple layers of shadow at varying offsets for a more refined glow
        shadow_offsets = [(3, 3), (2, 2), (-2, -2), (2, -2), (-2, 2), (3, 2), (2, 3)]
        for offset in shadow_offsets:
            shadow_text = TITLE_FONT.render("Realms of Fate", True, DARK_GOLD)
            shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + offset[0], HEIGHT//4 - 30 + offset[1]))
            SCREEN.blit(shadow_text, shadow_rect)
            
        title_text = TITLE_FONT.render("Realms of Fate", True, GOLD)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4 - 30))
        SCREEN.blit(title_text, title_rect)
        
        # Draw subtitle with similar treatment
        for offset in shadow_offsets[:4]:  # Fewer shadow layers for subtitle
            subtitle_shadow = SUBTITLE_FONT.render("Chronicles Unbound", True, DARK_GOLD)
            subtitle_shadow_rect = subtitle_shadow.get_rect(center=(WIDTH//2 + offset[0], HEIGHT//4 + 30 + offset[1]))
            SCREEN.blit(subtitle_shadow, subtitle_shadow_rect)
        
        subtitle_text = SUBTITLE_FONT.render("Chronicles Unbound", True, GOLD)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 30))
        SCREEN.blit(subtitle_text, subtitle_rect)
        
        # Draw decorative divider with animated shimmer effect
        current_time = pygame.time.get_ticks()
        shimmer_pos = (math.sin(current_time * 0.001) * 0.5 + 0.5) * (WIDTH*2//3 - WIDTH//3)
        for x in range(WIDTH//3, WIDTH*2//3):
            # Calculate distance from shimmer position
            dist = abs(x - (WIDTH//3 + shimmer_pos))
            if dist < 50:
                # Brighten color based on proximity to shimmer position
                bright_factor = 1.0 - (dist / 50)
                color = (
                    min(255, int(GOLD[0] * (1 + bright_factor * 0.5))),
                    min(255, int(GOLD[1] * (1 + bright_factor * 0.5))),
                    min(255, int(GOLD[2] * (1 + bright_factor)))
                )
            else:
                color = GOLD
            
            pygame.draw.line(SCREEN, color, (x, HEIGHT//3 + 50), (x+1, HEIGHT//3 + 50), 2)
        
        # Draw ornamental details with animated pulsing
        pulse = (math.sin(current_time * 0.002) * 0.3) + 0.7
        pulse_size = int(6 * pulse)
        for x in [WIDTH//3, WIDTH*2//3]:
            pygame.draw.circle(SCREEN, GOLD, (x, HEIGHT//3 + 50), pulse_size)
            # Add small rune marks around the circle
            for i in range(4):
                angle = math.radians(i * 90)
                px = x + math.cos(angle) * (pulse_size + 5)
                py = HEIGHT//3 + 50 + math.sin(angle) * (pulse_size + 5)
                pygame.draw.circle(SCREEN, GOLD, (int(px), int(py)), 2)
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(SCREEN)
        
        # Add version info with better styling
        version_font = pygame.font.SysFont("serif", 20)
        version_text = version_font.render("Version 0.1 Alpha", True, GOLD)
        version_shadow = version_font.render("Version 0.1 Alpha", True, DARK_GOLD)
        version_rect = version_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
        shadow_rect = version_shadow.get_rect(bottomright=(WIDTH - 19, HEIGHT - 19))
        SCREEN.blit(version_shadow, shadow_rect)
        SCREEN.blit(version_text, version_rect)
        
        # Draw a custom cursor instead of the default one
        if CURSOR_IMG:
            cursor_rect = CURSOR_IMG.get_rect(center=pygame.mouse.get_pos())
            SCREEN.blit(CURSOR_IMG, cursor_rect)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Run the main menu loop."""
        while True:
            # Handle events
            state_change = self.handle_events()
            if state_change:
                return state_change
            
            # Update
            self.update()
            
            # Draw
            self.draw()