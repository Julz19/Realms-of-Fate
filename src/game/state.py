"""
Game state management.
"""

class GameState:
    """Manages the overall game state."""
    
    def __init__(self):
        self.current_state = "main_menu"
        self.player = None
        self.game_world = None
        self.save_data = {}
    
    def change_state(self, new_state):
        """Change the current game state."""
        self.current_state = new_state
        print(f"Game state changed to: {new_state}")
    
    def load_game(self, save_id):
        """Load a saved game."""
        # This would load game data from a file
        print(f"Loading game save: {save_id}")
        # Set current state to gameplay
        self.current_state = "gameplay"
    
    def save_game(self, save_id):
        """Save the current game state."""
        # This would save game data to a file
        print(f"Saving game as: {save_id}")
    
    def new_game(self):
        """Start a new game."""
        # Initialize player, world, etc.
        self.player = {}  # This would be a Player object
        self.game_world = {}  # This would be a GameWorld object
        # Set current state to gameplay
        self.current_state = "gameplay"
        print("Starting new game")
    
    def exit_game(self):
        """Clean up and exit the game."""
        # Save any unsaved data, clean up resources, etc.
        print("Exiting game")