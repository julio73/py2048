import sys
import tty

class KeypressUtils:
    """Manages key input from the user."""
    
    def __init__(self):
        self.is_windows = False
        
        try:
            import msvcrt
            self.imp = msvcrt
            self.is_windows = True
        except ImportError:
            import termios
            self.imp = termios
        
    def getch_(self):
        """Get a single character input from user."""    
        if self.is_windows:
            ch = self.imp.getch()
            #TODO: implement/test windows
        else:
            fd = sys.stdin.fileno()
            old_settings = self.imp.tcgetattr(fd)
            try:
                tty.setraw(fd)
                self.imp.tcflush(sys.stdin, self.imp.TCIOFLUSH)
                ch = sys.stdin.read(1)
                
                if ch == '\x1b':
                    ch = self.getch_()
                    if ch == '[':
                        ch = self.getch_()
                elif ch == '\x03':
                    raise KeyboardInterrupt
                elif ch == '\x04':
                    raise EOFError
                return ch
            finally:
                self.imp.tcsetattr(fd, self.imp.TCSADRAIN, old_settings)
