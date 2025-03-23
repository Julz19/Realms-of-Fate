"""
Realms of Fate: Chronicles Unbound

Main entry point for the game.
"""
import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Import game components
from src.ui.menu import MainMenu
from src.game.state import GameState

def main():
    """Main entry point for the game."""
    # Set up the game state
    game_state = GameState()
    
    # Start with the main menu
    menu = MainMenu()
    
    # Main game loop
    while True:
        # Get the current state
        current_state = game_state.current_state
        
        # Handle different game states
        if current_state == "main_menu":
            # Run the main menu
            next_state = menu.run()
            
            # Handle menu selection
            if next_state == "new_game":
                game_state.new_game()
            elif next_state == "load_game":
                # For now, just load a dummy save
                game_state.load_game("save_001")
            elif next_state == "settings":
                game_state.change_state("settings")
                
        elif current_state == "gameplay":
            # This would run the actual gameplay
            # For now, just go back to the main menu
            print("Gameplay would run here")
            game_state.change_state("main_menu")
            
        elif current_state == "settings":
            # This would show the settings menu
            # For now, just go back to the main menu
            print("Settings menu would show here")
            game_state.change_state("main_menu")
            
        # Check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()