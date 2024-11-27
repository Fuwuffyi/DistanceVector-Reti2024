import copy
from collections import OrderedDict

class Router:
    # The router's identificator
    id: str

    # The links between this router and another
    # The frozenset contains source and dest
    # The integer rapresents the cost of that link
    links: set[tuple[frozenset[str], int]]

    # The routing table is a dictionary of which
    # the key is the pair source, dest,
    # the value is the next hop and the cost of it
    routing_table: OrderedDict[frozenset[str], tuple[str, int]]

    def __init__(self, identificator: str) -> None:
        self.id = identificator
        self.routing_table = OrderedDict()
        self.links = set()
        # Adds itself to the table at cost 0
        self.links.add((frozenset([self.id, self.id]), 0))

    def add_link(self, link: tuple[frozenset[str], int]) -> None:
        self.links.add(link)
        for r in link[0]:
            if (r == self.id):
                continue
            self.routing_table[link[0]] = (r, link[1])

    def get_frozen_table(self) -> OrderedDict[frozenset[str], tuple[str, int]]:
        return copy.deepcopy(self.routing_table)

    def __str__(self) -> str:
        output: str = f"Table for: {self.id}\n"
        for link, val in self.routing_table.items():
            filtered_link: list[str] = [item for item in link if item != self.id]
            output += f"Dest: {filtered_link[0]}, Next: {val[0]}, Cost: {val[1]}\n"
        return output 
