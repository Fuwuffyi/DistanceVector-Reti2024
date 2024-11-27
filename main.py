#!/bin/python

import curses
from router import Router
from collections import OrderedDict
from networkmanager import read_network_file

def run_distance_vector(routers: dict[str, Router], t_max: int):
    tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = dict()
    for t in range(0, len(routers)):
        # Create the new container for the tables at t
        tables[t] = OrderedDict()
        # Run the algorithm
        for id, router in routers.items():
            # Check all the other connected routers
            neighbors: set[str] = router.get_neighbors()
            # Send the current routing table to all other neighbors
            for other_id in neighbors:
                routers[other_id].update_table(sender_id=id, sender_table=router.get_frozen_table())
        # Save all the router's tables
        for id, router in routers.items():
            tables[t][id] = router.get_frozen_table()
    return tables

if __name__ == '__main__':
    # Read the current network configuration
    routers: dict[str, Router] = read_network_file("test_network.txt")
    # Run the algorithm and save all the steps
    tables: dict[int, OrderedDict[frozenset[str], tuple[str, int]]] = run_distance_vector(routers=routers, t_max=len(routers))
    
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
            # Refresh the screepair source, dest,n
            stdscr.refresh()

    # TODO: uncomment once UI is done
    # Start the UI
    # curses.wrapper(main)
    # tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = dict()
    for time, curr_tables in tables.items():
        print(f"Tables at time: {time}")
        for router_id, routing_table in curr_tables.items():
            print(f"Table for: {router_id}")
            for dest in routers:
                if dest == router_id:
                    print(f"Dest: {dest}, N.Hop: NONE, Cost: 0")
                else:
                    next_hop, cost = routing_table.get(dest) if dest in routing_table else ("NONE", "INF")
                    print(f"Dest: {dest}, N.Hop: {next_hop}, Cost: {cost if cost else 'INF'}")
