#!/bin/python

import curses
import ui 
from router import Router
from collections import OrderedDict
from networkmanager import read_network_file

def run_distance_vector(routers: dict[str, Router], t_max: int) -> dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]]:
    tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = dict()
    # Initialize T=0
    tables[0] = OrderedDict()
    for id, router in routers.items():
        tables[0][id] = router.get_frozen_table()
    t: int = 1
    while t < t_max:
        # Create the new container for the tables at t
        tables[t] = OrderedDict()
        # Send all messages (routing tables) to the network
        network: dict[tuple[str, str], OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = dict()
        for id, router in routers.items():
            # Check all the other connected routers
            neighbors: set[str] = router.get_neighbors()
            # Send the current routing table to all other neighbors
            for other_id in neighbors:
                network[(id, other_id)] = router.get_frozen_table()
        # Recieve all routing tables from the network
        for (sender_id, receiver_id), table in network.items():
            routers[receiver_id].update_table(sender_id=sender_id, sender_table=table)
        # Save current routing tables to dict
        for id, router in routers.items():
            tables[t][id] = router.get_frozen_table()
        t += 1
    return tables

if __name__ == '__main__':
    # Read the current network configuration
    routers: dict[str, Router] = read_network_file("test_network.txt")
    # Run the algorithm and save all the steps
    tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = run_distance_vector(routers=routers, t_max=len(routers))
    # Initialize the UI
    stdscr = ui.init()
    # Create the window to make sure it is the right dimensions
    cursor_position: tuple[int, int] = (0, 0)
    total_pages: int = len(tables) - 1
    # Draw the UI
    ui.draw(stdscr, cursor_position, total_pages, tables)
    quit_ui: bool = False
    while not quit_ui:
        # Get user input
        cursor_position = ui.handle_user_input(stdscr, cursor_position, total_pages, len(routers))
        if cursor_position[0] == -1:
            quit_ui = True
        else:
            ui.draw(stdscr, cursor_position, total_pages, tables)
    curses.endwin()
