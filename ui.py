import curses
from curses import textpad
from collections import OrderedDict
from typing import Final

HEADER_HEIGHT: Final[int] = 3

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

def handle_user_input(stdscr: curses.window, cursor_position: tuple[int, int], total_pages: int, router_count: int) -> tuple[int, int]:
    # Read key input from user
    rows, cols = stdscr.getmaxyx()
    key: int = stdscr.getch()
    # Exit if q or esc pressed
    if key == ord('q') or key == 27:
        return (-1, -1)
    elif key == ord('d') or key == curses.KEY_RIGHT:
        # Next page
        return ((cursor_position[0] + 1) % (total_pages + 1), cursor_position[1])
    elif key == ord('a') or key == curses.KEY_LEFT:
        # Previous page
        return ((cursor_position[0] - 1) % (total_pages + 1), cursor_position[1])
    elif key == ord('w') or key == curses.KEY_UP:
        # Scroll up
        return (cursor_position[0], max(cursor_position[1] - 1, 0))
    elif key == ord('s') or key == curses.KEY_DOWN:
        # Scroll down
        return (cursor_position[0], min(cursor_position[1] + 1, (router_count + 1) * router_count + router_count - (rows - HEADER_HEIGHT - 1)))
    elif key == ord('h'):
        # Show help menu
        stdscr.clear()
        stdscr.addstr(1, 1, "Help: Use 'a/arrow left' for previous page, 'd/arrow right' for next page, 'q/esc' to quit.")
        stdscr.refresh()
        stdscr.getch()
    return cursor_position

def draw(stdscr: curses.window, cursor_position: tuple[int, int], total_pages: int, routing_tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]]) -> None:
    stdscr.clear()
    draw_header(stdscr, cursor_position[0], total_pages)
    draw_content(stdscr, cursor_position[1], routing_tables[cursor_position[0]])
    stdscr.refresh()

def draw_header(stdscr: curses.window, page: int, total_pages: int) -> None:
    # Get screen width and height
    rows, cols = stdscr.getmaxyx()
    header_x, header_y = 1, 0
    header_width: int = cols - 2
    # Page navigation arrows and current page info
    left_arrow: str = "◀"
    right_arrow: str = "▶"
    page_info: str = f"{left_arrow} Routing tables at T={page} of {total_pages} {right_arrow}"
    # Center the page info in the header
    centered_page_info: str = page_info.center(header_width)
    # Draw the header text in yellow
    stdscr.addstr(header_y + 1, (cols - len(centered_page_info)) // 2, centered_page_info[:header_width - 2])
    # Draw the header border
    textpad.rectangle(stdscr, header_y, header_x, header_y + HEADER_HEIGHT - 1, header_x + header_width - 1)

def draw_content(stdscr: curses.window, scroll_amount: int, routing_tables: OrderedDict[str, OrderedDict[str, tuple[str, int]]]) -> None:
    # Setup some variables for proper display size
    rows, cols = stdscr.getmaxyx()
    content_x, content_y = 1, HEADER_HEIGHT
    content_width: int = cols - 2
    content_height: int = rows - HEADER_HEIGHT
    # Draw the content border
    textpad.rectangle(stdscr, content_y, content_x, content_y + content_height - 1, content_x + content_width - 1)
    # Prepare routing table data
    formatted_lines: list[str] = []
    for router, destinations in routing_tables.items():
        formatted_lines.append(f"Router: {router}")
        for dest in routing_tables:
            stdscr.addstr(10, 3, f"{len(routing_tables)}")
            if dest == router:
                # Router is itself, put value to 0
                formatted_lines.append(f"Dest: {dest}, N.Hop: NONE, Cost: 0")
            else:
                # Get values from routing tables
                next_hop, cost = destinations.get(dest) if dest in destinations else ("NONE", "INF")
                formatted_lines.append(f"Dest: {dest}, N.Hop: {next_hop}, Cost: {cost}")
        formatted_lines.append(None)
    formatted_lines.pop()
    # Calculate max lines
    max_lines: int = content_height - 2
    total_lines: int = len(formatted_lines)
    scroll_amount: int = max(0, min(scroll_amount, total_lines - max_lines))
    visible_lines: int = formatted_lines[scroll_amount:scroll_amount + max_lines]
    line_y: int = content_y + 1
    for line in visible_lines:
        if line:
            stdscr.addstr(line_y, content_x + 1, line[:content_width - 2])
        else:
            stdscr.hline(line_y, content_x + 1, curses.ACS_HLINE, content_width - 2)
        line_y += 1
