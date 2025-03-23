"""
Button class for the UI.
"""
import math
import pygame
import sys
import os

# Add the root directory to the path so we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import GOLD, DARK_GOLD, MENU_FONT, BUTTON_SOUND, SCREEN

class Button:
    """Interactive button with visual effects."""
    
    def __init__(self, text, pos, size, color, hover_color, shadow_offset=4):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.shadow_offset = shadow_offset
        self.current_color = color
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.shadow_rect = pygame.Rect(pos[0] + shadow_offset, pos[1] + shadow_offset, size[0], size[1])
        self.is_hovered = False
        self.was_hovered = False
        self.pulse_counter = 0
        self.glow_surface = pygame.Surface((size[0] + 20, size[1] + 20), pygame.SRCALPHA)
    
    def draw(self, surface):
        """Draw the button with all visual effects."""
        # Draw glow effect when hovered
        if self.is_hovered:
            # Create glow surface
            alpha = int(abs(math.sin(self.pulse_counter * 0.1)) * 100) + 50
            self.glow_surface.fill((0, 0, 0, 0))  # Reset with transparency
            glow_rect = pygame.Rect(10, 10, self.size[0], self.size[1])
            pygame.draw.rect(self.glow_surface, (255, 215, 0, alpha), glow_rect, border_radius=12)
            
            # Apply blur by drawing multiple transparent rects
            for i in range(10):
                pygame.draw.rect(self.glow_surface, (255, 215, 0, 5), 
                               pygame.Rect(10-i, 10-i, self.size[0]+(i*2), self.size[1]+(i*2)), 
                               border_radius=12)
            
            # Blit the glow
            surface.blit(self.glow_surface, (self.pos[0]-10, self.pos[1]-10))
        
        # Draw shadow with transparency
        shadow_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, self.darker_red_with_alpha(), 
                        pygame.Rect(0, 0, self.size[0], self.size[1]), 
                        border_radius=12)
        surface.blit(shadow_surface, (self.pos[0] + self.shadow_offset, self.pos[1] + self.shadow_offset))
        
        # Draw main button with transparency
        button_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, self.current_color, 
                        pygame.Rect(0, 0, self.size[0], self.size[1]), 
                        border_radius=12)
        surface.blit(button_surface, self.pos)
        
        # Add a subtle border
        pygame.draw.rect(surface, DARK_GOLD, self.rect, width=2, border_radius=12)
        
        # Render text with better glow effect
        text_surf = MENU_FONT.render(self.text, True, GOLD)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Add multiple shadow layers for better glow effect
        for offset in [(2, 2), (1, 1), (2, 1), (1, 2)]:
            shadow_surf = MENU_FONT.render(self.text, True, DARK_GOLD)
            shadow_rect = shadow_surf.get_rect(center=(text_rect.centerx + offset[0], text_rect.centery + offset[1]))
            surface.blit(shadow_surf, shadow_rect)
        
        # Draw main text
        surface.blit(text_surf, text_rect)
        
        # Add decorative runes to the sides of the button when hovered
        if self.is_hovered:
            rune_color = GOLD
            rune_size = 8
            
            # Left side rune
            pygame.draw.circle(surface, rune_color, (self.rect.left - 15, self.rect.centery), rune_size)
            pygame.draw.line(surface, rune_color, 
                           (self.rect.left - 15, self.rect.centery - 10),
                           (self.rect.left - 15, self.rect.centery + 10), 2)
            
            # Right side rune
            pygame.draw.circle(surface, rune_color, (self.rect.right + 15, self.rect.centery), rune_size)
            pygame.draw.line(surface, rune_color, 
                           (self.rect.right + 15, self.rect.centery - 10),
                           (self.rect.right + 15, self.rect.centery + 10), 2)
    
    def darker_red_with_alpha(self):
        """Return darker red with proper alpha."""
        # Import colors here to avoid circular imports
        from config import DARKER_RED
        return (DARKER_RED[0], DARKER_RED[1], DARKER_RED[2], DARKER_RED[3])
    
    def update(self, mouse_pos, time_passed):
        """Update button state based on mouse position."""
        previous_hover = self.is_hovered
        
        if self.rect.collidepoint(mouse_pos):
            # Smoother transition effect when hovering
            target_color = self.hover_color
            current = pygame.Color(self.current_color[0], self.current_color[1], 
                                 self.current_color[2], self.current_color[3])
            target = pygame.Color(target_color[0], target_color[1], 
                                target_color[2], target_color[3])
            
            # Interpolate color values for smoother transition
            self.current_color = current.lerp(target, 0.1)
            self.is_hovered = True
            self.pulse_counter += time_passed
            
            # Play sound when first hovering
            if not previous_hover and BUTTON_SOUND:
                BUTTON_SOUND.play()
        else:
            # Smooth transition back to normal color
            target_color = self.color
            current = pygame.Color(self.current_color[0], self.current_color[1], 
                                 self.current_color[2], self.current_color[3])
            target = pygame.Color(target_color[0], target_color[1], 
                                target_color[2], target_color[3])
            
            self.current_color = current.lerp(target, 0.1)
            self.is_hovered = False
        
    def handle_event(self, event):
        """Handle mouse events on the button."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            # Import here to avoid circular imports
            from src.ui.effects import particle_effect
            
            # Create particles when clicked
            particle_effect(SCREEN, (self.rect.centerx, self.rect.centery), GOLD, 3, 15)
            
            # Play a different sound for click
            if BUTTON_SOUND:
                BUTTON_SOUND.set_volume(0.7)
                BUTTON_SOUND.play()
            return True
        return False