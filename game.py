import random
import copy

import displayutils
import keypressutils

class Game:
    """Python 2048 game"""
    
    def __init__(self):
        """Initialize a new game instance."""
        self.__initialize()
    
    def __initialize(self):
        self._grid = {
            1:{1:0,2:0,3:0,4:0},
            2:{1:0,2:0,3:0,4:0},
            3:{1:0,2:0,3:0,4:0},
            4:{1:0,2:0,3:0,4:0}
        }
        self._winning_tile = 2048
        self._score = 0
        self._gameover = False
        self._continue = False
        self._won = False
        self._dist = [2,2,2,2,2,2,2,2,2,4]
        
    
    def start_game(self):
        """Start the game instance."""
        self._display = displayutils.DisplayUtils()
        self._keypress = keypressutils.KeypressUtils()
        
        self._display.load_layout_file()
        self.add_random_tile()
        self.add_random_tile()
        self.refresh_game_board()
    
        try:
            while not self.is_game_over():
                direction = self.get_next_move()
                if direction in ['A','B','C','D']:
                    old_values = self.get_tile_values()
                    self.move_in_direction(direction)
                    new_values = self.get_tile_values()
                    if old_values != new_values:
                        self.add_random_tile()
                        self.refresh_game_board()
                    if (not self._continue
                            and self._winning_tile in new_values):
                        self._won = True
                        self._display.display_game_board(
                            get_values_with_highlighted_target(self._grid, self._winning_tile),
                            self._score)
                        print "You won! You have reached tile", self._winning_tile
                        self.want_to_continue(False)
            else:
                self.end_game()
        except EOFError:
            print "Game ended."
        except KeyboardInterrupt:
            print "Game ended."
    
    def refresh_game_board(self):
        """Refresh the game's board with tile values and score."""
        self._display.display_game_board(self.get_tile_values(), self._score)
    
    def get_tile_values(self):
        """Get the values of all tiles."""
        return [tile
                    for rows in self._grid.itervalues()
                        for tile in rows.itervalues()]
    
    def get_available_tiles(self):
        """Get all tiles that are available i.e. with 0 as value."""
        return [(x, y)
                    for x, rows in self._grid.iteritems()
                        for y, tile in rows.iteritems()
                            if tile == 0]
    
    def add_random_tile(self):
        """Add one default tile at any available location on the grid."""
        remaining = self.get_available_tiles()
        if remaining:
            (x, y) = random.choice(remaining)
            self._grid[x][y] = random.choice(self._dist)
        
    def want_to_continue(self, already_asked):
        """Ask user if they want to continue."""
        if not already_asked:
            print "Do you want to continue? Press 'y' or 'n'."
        response = self._keypress.getch_()
        if response == "y" or response == "Y":
            print response, "-> 'Yep'"
            self._continue = True
            self.refresh_game_board()
        elif response == "n" or response == "N":
            print response, "-> 'Nope'"
            self._continue = False
            self._gameover = True
        else:
            self.want_to_continue(True)
    
    def is_game_over(self):
        """True when the board is filled and no move is possible."""
        self._gameover = (self._gameover
                          or (not self.get_available_tiles()
                              and not self.has_available_matches()))
        return self._gameover
        
    def get_next_move(self):
        """Request the next move from the user."""
        return self._keypress.getch_()
    
    def has_available_matches(self):
        """True when any merger of two tiles is possible."""
        rows_a = [v.values() for v in self._grid.itervalues()]
        rows_t = [v.values() for v in transpose_grid(self._grid).itervalues()]
        for lines in [rows_a, rows_t]:
            for line in lines:
                (_, pts) = squash_line(line, True)
                if pts != 0:
                    return True
        return False

    def end_game(self):
        """End the game."""
        #TODO: Store scores maybe.
        if not self._won:
            print "Game over!"
        print "Final score: ", self._score
        self.ask_about_another_round(False)
    
    def ask_about_another_round(self, already_asked):
        if not already_asked:
            print "Start new game? Press 'y' or 'n'."
        response = self._keypress.getch_()
        if response == "y" or response == "Y":
            print response, "-> 'Yep'"
            self.__initialize()
            self.start_game()
        elif response == "n" or response == "N":
            print response, "-> 'Nope'"
            self._continue = False
            self._gameover = True
        else:
            self.ask_about_another_round(True)
        
        
    
    def move_in_direction(self, direction):
        (grid, pts) = move_tiles(self._grid, direction)
        self._grid = grid
        self._score += pts

def squash_line(line, move_left):
    """
    Return a tuple of the new line and the scored points for making the move.  
    """
    points_added = 0
    if not move_left:
        line.reverse()
    tiles = [v for v in line if v != 0]
    merged = []
    i = 0
    while i < len(tiles):
        if i+1 < len(tiles) and tiles[i] == tiles[i+1]:
            value = tiles[i]*2
            points_added += value 
            merged.append(value)
            i+=2
            continue
        merged.append(tiles[i])
        i+=1
    
    deficit = len(line)-len(merged)
    merged.extend([0]*deficit)
    
    if not move_left:
        merged.reverse()
    
    return (merged, points_added)

def reconstruct_grid(new_rows):
    """Reconstruct the grid with the given rows."""
    default_grid = {
        1:{1:0,2:0,3:0,4:0},
        2:{1:0,2:0,3:0,4:0},
        3:{1:0,2:0,3:0,4:0},
        4:{1:0,2:0,3:0,4:0}
    }
    for (y, old_row) in default_grid.iteritems():
        new_row = new_rows[y-1]
        for x in old_row.iterkeys():
            default_grid[y][x] = new_row[x-1]
    
    return default_grid

def transpose_grid(old_grid):
    """Transpose the given grid. Must be a rectangle (ideally square) grid."""
    new_grid = {}
    for (y, row) in old_grid.iteritems():
        for x in row.iterkeys():
            if x not in new_grid:
                new_grid[x] = {}
            new_grid[x][y] = old_grid[y][x]
    
    return new_grid

def get_values_with_highlighted_target(original_grid, target_value):
    """Returns values with highlighted tiles with target value."""
    old_rows = [v.values() for v in original_grid.itervalues()]
    grid_copy = reconstruct_grid(old_rows)
    target_tiles = [(row, col)
                        for row in grid_copy.iterkeys()
                            for col in grid_copy[row].iterkeys()
                                if grid_copy[row][col] == target_value]
    for tile in target_tiles:
        (row, col) = tile
        for hk in grid_copy[row].iterkeys(): # hk = horizontal keys
            tile_value = grid_copy[row][hk]
            if not str(tile_value).isdigit(): # cross section
                grid_copy[row][hk] = '+'
            elif str(tile_value) == str(target_value):
                pass
            else:
                distance = hk - col
                if distance == -1:
                    grid_copy[row][hk] = '->'
                elif distance == 1:
                    grid_copy[row][hk] = '<-'
                else:
                    grid_copy[row][hk] = '--'
        for vk in grid_copy.iterkeys(): # vk = vertical keys
            tile_value = grid_copy[vk][col]
            if not str(tile_value).isdigit(): # cross section
                grid_copy[vk][col] = '+'
            elif str(tile_value) == str(target_value):
                pass
            else:
                distance = vk - row
                if distance == -1:
                    grid_copy[vk][col] = 'v'
                elif distance == 1:
                    grid_copy[vk][col] = '^'
                else:
                    grid_copy[vk][col] = '|'
    
#     for line in [v.values() for v in grid_copy.itervalues()]:
#         print line
#     
    return [tile
                for rows in grid_copy.itervalues()
                    for tile in rows.itervalues()]

def move_tiles(grid, direction):
    """
    Move the tiles of the given grid in the given direction.
    Return the points scored from moving.
    """
    move_left = (direction == 'D' or direction == 'A')
    rows = []
    if direction == 'D': #left
        rows = [v.values() for v in grid.itervalues()]
        rows_and_pts = [squash_line(r, move_left) for r in rows]
        new_rows = [tpl[0] for tpl in rows_and_pts]
        grid = reconstruct_grid(new_rows)
    elif direction == 'C': #right
        rows = [v.values() for v in grid.itervalues()]
        rows_and_pts = [squash_line(r, move_left) for r in rows]
        new_rows = [tpl[0] for tpl in rows_and_pts]
        grid = reconstruct_grid(new_rows)
    elif direction == 'A': #up
        rows = [v.values() for v in transpose_grid(grid).itervalues()]
        rows_and_pts = [squash_line(r, move_left) for r in rows]
        new_rows = [tpl[0] for tpl in rows_and_pts]
        grid = transpose_grid(reconstruct_grid(new_rows))
    elif direction == 'B': #down
        rows = [v.values() for v in transpose_grid(grid).itervalues()]
        rows_and_pts = [squash_line(r, move_left) for r in rows]
        new_rows = [tpl[0] for tpl in rows_and_pts]
        grid = transpose_grid(reconstruct_grid(new_rows))        
    
    pts_for_move = sum([tpl[1] for tpl in rows_and_pts], 0)
    
    return (grid, pts_for_move)