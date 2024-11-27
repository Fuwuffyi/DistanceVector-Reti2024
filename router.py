import copy
from collections import OrderedDict

class Router:
    # The router's identificator
    id: str

    # The links between this router and another
    # The frozenset contains source and dest
    # The integer rapresents the cost of that link
    links: dict[frozenset[str], int]

    # The routing table is a dictionary of which
    # the key is the destination
    # the value is the next hop and the cost of it
    routing_table: OrderedDict[str, tuple[str, int]]

    def __init__(self, identificator: str) -> None:
        self.id = identificator
        self.routing_table = OrderedDict()
        self.links = dict()
        # Adds itself to the table at cost 0
        self.routing_table[self.id] = (self.id, 0)
        self.links[frozenset([self.id, self.id])] = 0

    def add_link(self, link: tuple[frozenset[str], int]) -> None:
        self.links[link[0]] = link[1]
        for r in link[0]:
            if (r == self.id):
                continue
            self.routing_table[r] = (r, link[1])

    def get_frozen_table(self) -> OrderedDict[str, tuple[str, int]]:
        return copy.deepcopy(self.routing_table)

    def get_neighbors(self) -> set[str]:
        return {neighbor for link in self.links for neighbor in link if neighbor != self.id}

    def update_table(self, sender_id: str, sender_table: OrderedDict[str, tuple[str, int]]) -> None:
        current_link_weight: int = self.links[frozenset([sender_id, self.id])]
        for dest, connection in sender_table.items():
            pass
