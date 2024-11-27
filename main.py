#!/bin/python

import curses
from router import Router
from networkmanager import read_network_file

def main(stdscr: curses.window) -> any:
    # Read the current network configuration
    routers: dict[str, Router] = read_network_file("test_network.txt")
    # Simulate the algorithm (just run through it with tMax = len(routers) for convergence)
    for i in range(1, len(routers) + 1):
        print(f"Routing table at t={i}")
        for id, router in routers.items():
            print(router)
    # Set some flags for the UI
    curses.curs_set(0)
    stdscr.nodelay(0)
    stdscr.timeout(100)
    cursor_position: tuple[int, int] = (0, 0)
    # Draw the UI
    while True:
        # Get user input
        key = stdscr.getch()
        # Exit on Q
        if key == ord('q'):
            break
        elif key == curses.KEY_RIGHT or key == ord('d'):
            # Move RIGHT
            cursor_position = (cursor_position[0] + 1, cursor_position[0])
        elif key == curses.KEY_LEFT or key == ord('a'):
            # Move LEFT 
            cursor_position = (cursor_position[0] - 1, cursor_position[0])
        elif key == curses.KEY_UP or key == ord('w'):
            # Move UP 
            cursor_position = (cursor_position[0], cursor_position[0] - 1)
        elif key == curses.KEY_DOWN or key == ord('s'):
            # Move DOWN 
            cursor_position = (cursor_position[0], cursor_position[0] + 1)
        # Clear the screen
        stdscr.clear()
        # TODO: remove once UI is finished
        stdscr.addstr(0, 0, f"Current pos: {cursor_position}")
        # Refresh the screen
        stdscr.refresh()

if __name__ == '__main__':
    # Start the UI
    curses.wrapper(main)
