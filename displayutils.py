import os
import subprocess

class DisplayUtils:
    """drawing 2048 stuff"""
    
    def __init__(self, layout_id):
        """Initialize the class instance."""
        self._layout_id = layout_id
        self._tile_placeholders = ['.', ' ', ' ', ' ']
        self._tile_widths = [1,6,9,13] 
        self._layout_locations = {
            1: 'layouts/clean.lay',
            2: 'layouts/small.lay',
            3: 'layouts/medium.lay',
            4: 'layouts/large.lay'
        }
        self.load_layout_file()
    
    def clear_screen(self):
        """Start subprocess for clear screen signal."""
        if os.name == 'nt':
            subprocess.call('cls')
        else:
            subprocess.call('clear')
    
    def load_layout_file(self):
        """Load the file layout from the given location."""
        file_path  = self._layout_locations[self._layout_id]
        with open(file_path, 'r') as layout_file:
            self._layout = ''.join(layout_file)
            self.format_layout()
    
    def format_layout(self):
        """Formats the current layout."""
        new_layout = self._layout
        w = self._tile_widths[self._layout_id-1]
        new_layout = new_layout.replace('\t+', '-'*w+'+')
        new_layout = new_layout.replace('\t|', ' '*w+'|')
        self._layout = new_layout
    def display_game_board(self, values, score): 
        """Display the game board using the loaded layout."""
        if self._layout is not None:
            self.clear_screen()
            formatted_values = [self.format_tile_value(v) for v in values]
            print self._layout.format(*formatted_values+[score])
    
    def format_tile_value(self, tile_value):
        """Format the tile value."""
        w = self._tile_widths[self._layout_id-1]
        p = self._tile_placeholders[self._layout_id-1]
        if tile_value == 0:
            return str(p) * w
        else:
            v = str(tile_value)
            pad = int((w - len(v))/2)
            left = pad
            right = w - len(v) - pad
            return p*left + v + p*right
