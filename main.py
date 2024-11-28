#!/bin/python

import ui
import json
import curses
from router import Router
from collections import OrderedDict
from networkmanager import read_network_file

def run_distance_vector(routers: dict[str, Router], t_max: int) -> dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]]:
    tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = dict()
    # Initialize T=0
    tables[0] = OrderedDict()
    for id, router in routers.items():
        tables[0][id] = router.get_frozen_table()
    # Set exit variables
    done: bool = False
    t: int = 1
    # Run the algorithm
    while not done and t < t_max:
        # Create the new container for the tables at t
        tables[t] = OrderedDict()
        # Send all messages (routing tables) to the network
        network: dict[tuple[str, str], OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = dict()
        for id, router in routers.items():
            # Skip routers that have not been updated last t
            if not router.dirty_table:
                continue
            # Check all the other connected routers
            neighbors: set[str] = router.get_neighbors()
            # Send the current routing table to all other neighbors
            for other_id in neighbors:
                network[(id, other_id)] = router.get_frozen_table()
            # Set the router's dirty flag to false
            router.dirty_table = False
        # Recieve all routing tables from the network
        for (sender_id, receiver_id), table in network.items():
            routers[receiver_id].update_table(sender_id=sender_id, sender_table=table)
        # Save current routing tables to dict
        done = True
        for id, router in routers.items():
            tables[t][id] = router.get_frozen_table()
            if router.dirty_table:
                done = False
        t += 1
    # If early exit the last table will be same as previous
    if done == True:
        del tables[t - 1]
    return tables

def write_to_file(tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]]) -> None:
    # Transform the original structure into a different format
    transformed_data: dict[dict] = dict()
    for t, routers in tables.items():
        router_data = {
            "routers": {}
        }
        for router_id, routes in routers.items():
            router_table: list[dict] = []
            for destination, (next_hop, cost) in routes.items():
                router_table.append({
                    "destination": destination,
                    "next_hop": next_hop,
                    "cost": cost
                })
            router_data["routers"][router_id] = {
                "table": router_table
            }
        transformed_data[t] = router_data
    # Dump the transformed data to the output.json file
    with open('output.json', 'w') as file:
        json.dump(transformed_data, file, indent=3)

if __name__ == '__main__':
    # Read the current network configuration
    routers: dict[str, Router] = read_network_file("test_network.txt")
    # Run the algorithm and save all the steps
    tables: dict[int, OrderedDict[str, OrderedDict[str, tuple[str, int]]]] = run_distance_vector(routers=routers, t_max=len(routers))
    # Save the file locally
    write_to_file(tables)
    # Try opening a curses UI
    try:
        # Initialize the UI
        stdscr: curses.window = ui.init()
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
    except:
        print("You do not have the curses module (curses_windows for windows)")

