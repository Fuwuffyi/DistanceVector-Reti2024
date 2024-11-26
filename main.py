#!/bin/python

from router import Router
from networkmanager import read_network_file

if __name__ == '__main__':
    routers: dict[str, Router] = read_network_file("test_network.txt")
    for id, router in routers.items():
        print(router)
