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
        self.routing_table[frozenset([self.id, self.id])] = (self.id, 0)
        self.links.add((frozenset([self.id, self.id]), 0))

    def add_link(self, link: tuple[frozenset[str], int]) -> None:
        self.links.add(link)
        for r in link[0]:
            if (r == self.id):
                continue
            self.routing_table[link[0]] = (r, link[1])

    def get_frozen_table(self) -> OrderedDict[frozenset[str], tuple[str, int]]:
        return copy.deepcopy(self.routing_table)

    def get_neighbors(self) -> set[str]:
        return {neighbor for link in self.links for neighbor in link[0] if neighbor != self.id}

    def update_table(self, other_routing_table: OrderedDict[frozenset[str], tuple[str, int]]) -> None:
        pass
