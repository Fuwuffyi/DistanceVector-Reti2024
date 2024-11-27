import curses
from curses.textpad import rectangle as guirect

def init() -> curses.window:
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    # stdscr.nodelay()
    # stdscr.timeout(100)
    # curses.start_color()  # Initialize color support
    # curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Blue on black for header
    # curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # White on black for text
    # curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow for highlighting
    return stdscr

def handle_user_input(stdscr: curses.window, cursor_position: tuple[int, int], total_pages: int) -> tuple[int, int]:
    # Read key input from user
    key: int = stdscr.getch()
    # Exit if q or esc pressed
    if key == ord('q') or key == 27:
        return (-1, -1)
    elif key == ord('d') or key == curses.KEY_RIGHT:
        # Next page
        return (min(cursor_position[0] + 1, total_pages), cursor_position[1])
    elif key == ord('a') or key == curses.KEY_LEFT:
        # Previous page
        return (max(cursor_position[0] - 1, 0), cursor_position[1])
    elif key == ord('w') or key == curses.KEY_UP:
        # Scroll up
        return (cursor_position[0], max(cursor_position[1] - 1, 0))
    elif key == ord('s') or key == curses.KEY_DOWN:
        # Scroll down
        return (cursor_position[0], cursor_position[1] + 1) # TODO: add minimum here
    elif key == ord('h'):
        # Show help menu
        stdscr.clear()
        stdscr.addstr(1, 1, "Help: Use 'a/arrow left' for previous page, 'd/arrow right' for next page, 'q/esc' to quit.")
        stdscr.refresh()
        stdscr.getch()
    return cursor_position
