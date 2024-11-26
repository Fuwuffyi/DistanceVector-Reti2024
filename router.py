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
    routing_table: dict[frozenset[str], tuple[str, int]]

    def __init__(self, identificator: str):
        self.id = identificator
        self.links = set()
        self.routing_table = {}

    def add_link(self, link: tuple[frozenset[str], int]):
        self.links.add(link)
    
    def __str__(self) -> str:
        return f"Table for: {self.id}\n{self.routing_table}"
