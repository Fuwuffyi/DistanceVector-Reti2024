# Distance Vector - Routing Protocol Visualization
# > [!IMPORTANT]
### Running this code might output an error if the user does not have the curses module installed nor the windows-curses module installed it must be installed:
   ```bash
   pip install curses
   # OR
   pip install windows-curses
   ```
## Overview
This project is a simple python CLI application. It reads routing data and utilizes curses to fully display the routing protocol steps.
## Features
- **Curses UI**: The application has a simple UI to display the routing table information, and how it updates through time.
- **Responsive UI**: The user interface will resize automatically depending on the size of the terminal it is run on.
## Files
The project consists of multiple files:
1. **main.py**: This is the starting point of the code, it combines all other modules into one for ease of use.
2. **networkmanager.py**: This module reads the file given to it, and reads the router and link data.
3. **router.py**: This contains the router class, it has the routing table and connection data.
4. **ui.py**: This script contains the UI handling part of the ui.
## Requirements
- Python 3.x
- curses (or windows-curses)
## Usage
### Basic workflow
1. Open a terminal.
2. Navigate to the directory containing `main.py`.
3. Run the script:
   ```bash
   ./main.py test_network.txt
   # OR
   python main.py test_network.txt
   ```
4. The application will show the curses terminal UI, use the `h` key to show a help message.
5. You can scroll through the tables using the `mouse wheel` or the `up/down` arrows.
6. You can change page (the current time) using the `left/right` arrows.
7. Use q to quit.
### Network file specifications
The network file is written in two sections:
1. The first section contains all routers and their `ids`, the `id` is a case sensitive string (e.g.: `r A`).
2. The second section contains `links` between said routers, the `link` contains two router ids and the cost between them (e.g.: `l A B 4`).
Example:
```txt
r A
r B
r C
l A B 3
l B C 2
l A C 7
```
It will create a three node network, with costs: **3** (between A and B), **2** (between B and C) and **7** (between A and C)
