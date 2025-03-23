"""
Visual effects for the UI.
"""
import math
import random
import pygame
import sys
import os

# Add the root directory to the path so we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import WIDTH, HEIGHT, GOLD, SCREEN

def particle_effect(surface, pos, color, size, num_particles=8):
    """Draw elaborate particle effects for button interactions."""
    particles = []
    for i in range(num_particles):
        angle = math.radians(random.randint(0, 360))
        speed = random.uniform(2, 6)
        size = random.randint(2, 5)
        life = random.randint(20, 40)
        particles.append({
            'pos': [pos[0], pos[1]],
            'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
            'size': size,
            'color': color,
            'life': life
        })
    
    # Animation loop
    for _ in range(10):  # Just run for a few frames to get initial positions
        for p in particles:
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            p['life'] -= 1
            
    # Draw particles at final positions
    for p in particles:
        if p['life'] > 0:
            pygame.draw.circle(surface, p['color'], 
                             (int(p['pos'][0]), int(p['pos'][1])), 
                             p['size'])

def draw_decorative_frame(surface, rect, color, width=3, fancy=False):
    """Draw a decorative frame with corner embellishments."""
    # Main rectangle
    pygame.draw.rect(surface, color, rect, width=width, border_radius=10)
    
    if fancy:
        # More elaborate corner decorations
        corner_size = 25
        
        # Top left
        pygame.draw.line(surface, color, 
                        (rect.left - 5, rect.top + corner_size),
                        (rect.left + corner_size, rect.top - 5), width)
        pygame.draw.circle(surface, color, (rect.left, rect.top), 5)
        
        # Top right
        pygame.draw.line(surface, color, 
                        (rect.right + 5, rect.top + corner_size),
                        (rect.right - corner_size, rect.top - 5), width)
        pygame.draw.circle(surface, color, (rect.right, rect.top), 5)
        
        # Bottom left
        pygame.draw.line(surface, color, 
                        (rect.left - 5, rect.bottom - corner_size),
                        (rect.left + corner_size, rect.bottom + 5), width)
        pygame.draw.circle(surface, color, (rect.left, rect.bottom), 5)
        
        # Bottom right
        pygame.draw.line(surface, color, 
                        (rect.right + 5, rect.bottom - corner_size),
                        (rect.right - corner_size, rect.bottom + 5), width)
        pygame.draw.circle(surface, color, (rect.right, rect.bottom), 5)
        
        # Add decorative runes in the middle of each side
        pygame.draw.circle(surface, color, (rect.centerx, rect.top), 4)
        pygame.draw.circle(surface, color, (rect.centerx, rect.bottom), 4)
        pygame.draw.circle(surface, color, (rect.left, rect.centery), 4)
        pygame.draw.circle(surface, color, (rect.right, rect.centery), 4)

def create_ambient_particles():
    """Create ambient floating particles for background atmosphere."""
    particles = []
    for _ in range(30):
        particles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'size': random.uniform(1, 3),
            'speed': random.uniform(0.2, 1),
            'color': (
                random.randint(200, 255),  # R
                random.randint(180, 255),  # G
                random.randint(0, 100),    # B
                random.randint(20, 60)     # Alpha
            )
        })
    return particles

def update_ambient_particles(particles):
    """Update ambient particle positions and draw them."""
    for p in particles:
        p['y'] -= p['speed']
        if p['y'] < 0:
            p['y'] = HEIGHT
            p['x'] = random.randint(0, WIDTH)
        
        # Draw the particle
        pygame.draw.circle(
            SCREEN, 
            p['color'], 
            (int(p['x']), int(p['y'])), 
            int(p['size'])
        )