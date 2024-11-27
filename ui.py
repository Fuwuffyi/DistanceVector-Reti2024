import curses
from curses import textpad

def init() -> curses.window:
    stdscr: curses.window = curses.initscr()
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
        return ((cursor_position[0] + 1) % (total_pages + 1), 0)
    elif key == ord('a') or key == curses.KEY_LEFT:
        # Previous page
        return ((cursor_position[0] - 1) % (total_pages + 1), 0)
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

def draw(stdscr: curses.window, cursor_position: tuple[int, int], total_pages: int) -> None:
    stdscr.clear()
    draw_header(stdscr, cursor_position[0], total_pages)
    draw_content(stdscr, cursor_position)
    stdscr.refresh()

def draw_header(stdscr: curses.window, page: int, total_pages: int) -> None:
    # Get screen width and height
    rows, cols = stdscr.getmaxyx()
    header_x, header_y = 1, 0
    header_width: int = cols - 2
    header_height: int = 3
    # Page navigation arrows and current page info
    left_arrow: str = "◀"
    right_arrow: str = "▶"
    page_info: str = f"{left_arrow} Page {page} of {total_pages} {right_arrow}"
    # Center the page info in the header
    centered_page_info: str = page_info.center(header_width)
    # Draw the header text in yellow
    # stdscr.attron(curses.color_pair(3))
    stdscr.addstr(header_y + 1, (cols - len(centered_page_info)) // 2, centered_page_info)
    # stdscr.attroff(curses.color_pair(3))
    # Draw the header border
    textpad.rectangle(stdscr, header_y, header_x, header_y + header_height - 1, header_x + header_width - 1)

def draw_content(stdscr: curses.window, cursor_position: tuple[int, int]) -> None:
    pass
