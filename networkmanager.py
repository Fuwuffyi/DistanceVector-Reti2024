from router import Router

# Reads a network file to get the configuration of a network
# The file must be formatted as follows:
#
# The first section contains the routers and their ids:
# r <id>
#
# The second section contains the links and costs between the routers:
# l <id1> <id2> <cost>
def read_network_file(filename: str) -> dict[str, Router]:
    routers: dict[str, Router] = {}
    with open(filename, 'r') as network_file:
        for line in network_file:
            line: str = line.strip()
            if line.startswith('r '):
                router_id: stri = line[2:].strip()
                router: Router = Router(router_id)
                routers[router_id] = router
            if line.startswith('l '):
                parts: str = line.split()
                id1: str = parts[1].strip()
                id2: str = parts[2].strip()
                cost: int = int(parts[3].strip())
                router1: Router = routers.get(id1)
                router2: Router = routers.get(id2)
                if router1 and router2:
                    link: tuple[frozenset[str], int] = (frozenset([id1, id2]), cost)
                    router1.add_link(link)
                    router2.add_link(link)
    return routers
