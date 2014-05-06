import sys
import game

#TODO: implement proper layout selection, and other options.
if __name__ == '__main__':
    if sys.argv[1:]:
        layout_id = sys.argv[1]
        if layout_id.isdigit():
            g = game.Game(int(layout_id))
            g.start_game()
    else:
        g = game.Game()
        g.start_game()
