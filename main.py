#!/bin/python

import curses
from router import Router
from collections import OrderedDict
from networkmanager import read_network_file

if __name__ == '__main__':
    # Read the current network configuration
    routers: dict[str, Router] = read_network_file("test_network.txt")
    # Dictionary to save all the steps through the algorithm
    tables: dict[int, OrderedDict[frozenset[str], tuple[str, int]]] = dict()
    # Simulate the algorithm (just run through it with tMax = len(routers) for convergence)
    for t in range(0, len(routers)):
        # Create the new container for the tables at t
        tables[t] = OrderedDict()
        # TODO: implement algorithm
        # Save all the router's tables
        for id, router in routers.items():
            tables[t][frozenset([id])] = router.get_frozen_table()

    # Function used to draw the UI
    def main(stdscr: curses.window) -> any:
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
                cursor_position = (cursor_position[0] + 1 if cursor_position[0] + 1 < len(routers) else len(routers) - 1, cursor_position[1])
            elif key == curses.KEY_LEFT or key == ord('a'):
                # Move LEFT 
                cursor_position = (cursor_position[0] - 1 if cursor_position[0] - 1 >= 0 else 0, cursor_position[1])
            elif key == curses.KEY_UP or key == ord('w'):
                # Move UP 
                cursor_position = (cursor_position[0], cursor_position[1] - 1 if cursor_position[1] - 1 >= 0 else 0)
            elif key == curses.KEY_DOWN or key == ord('s'):
                # Move DOWN 
                cursor_position = (cursor_position[0], cursor_position[1] + 1) # TODO: add other bound
            # Clear the screen
            stdscr.clear()
            # Draw the UI
            stdscr.addstr(0, 0, f"Current page: t = {cursor_position[0]}")
            # Refresh the screen
            stdscr.refresh()

    # TODO: uncomment once UI is done
    # Start the UI
    # curses.wrapper(main)
    for t, time_tables in tables.items():
        print(f"Tables at time: t = {t}")
        for s_id, table in time_tables.items():
            id: str = list(s_id)[0]
            print(f"Table for: {id}")
            for s_router_id in [frozenset([r, id]) for r in routers]:
                router_id: list[str] | str = [item for item in s_router_id if item != id]
                router_id = router_id[0] if len(router_id) > 0 else id
                if router_id == id:
                    print(f"Dest: {router_id}, N.Hop: {router_id}, Cost: 0")
                else:
                    print(f"Dest: {router_id}, N.Hop: {table[s_router_id][0] if s_router_id in table else "NONE"}, Cost: {table[s_router_id][1] if s_router_id in table else "INF"}")
                

