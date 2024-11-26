class Router:
    # The router's identificator
    id: str

    # The links between this router and another
    # The frozenset contains source and dest
    # The integer rapresents the cost of that link
    links: set[tuple(frozenset(), int)]

    # The routing table is a dictionary of which
    # the key is the pair source, dest,
    # the value is the next hop and the cost of it
    routing_table: dict[frozenset(), tuple(str, int)]

    def __init__(self, identificator: str, start_links: set[tuple(frozenset(), int)]):
        self.id = identificator
        self.links = start_links
        self.routing_table = {}
    
    def __str__(self):
        return f"Table for: {self.id}\n{self.routing_table}"
