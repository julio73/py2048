import os
import subprocess

class DisplayUtils:
    """drawing 2048 stuff"""
    
    TILE_PLACEHOLDER = '.'
    
    def __init__(self):
        self._layout = None
    
    def clear_screen(self):
        if os.name == 'nt':
            subprocess.call('cls')
        else:
            subprocess.call('clear')
    
    def load_layout_file(self, location='layouts/clean.lay'):
        """Load the file layout from the given location."""
        with open(location,'r') as layout_file:
            self._layout = ''.join(layout_file)

    def display_game_board(self, values, score): 
        """Display the game board using the loaded layout."""
        if self._layout is not None:
            self.clear_screen()
            formatted_values = [self.format_tile_value(v) for v in values]
            print self._layout.format(*formatted_values+[score])
    
    def format_tile_value(self, tile_value):
        if tile_value == 0:
            return str(self.TILE_PLACEHOLDER)
        else:
            return str(tile_value)
    
    
        
    