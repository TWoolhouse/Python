import config as cfg
from log import log

import enum

import libs
import iofile
from vector import Vector
import randstate

cfg.load("structure")
shapes = list()

def generate(grid):
    global shapes
    log.info("Generating Structures")
    grid("random").load()

    zones = []
    for cell in grid.all():
        if cell["zone"] and cell["zone"] not in zones:
            zones.append(cell["zone"])

    grid("dispatch").new("Structure", func=GenStructure)
    for zone in zones:
        grid("dispatch")["Structure"] = (zone, randstate.Random(grid("random").generate()))
    grid("dispatch")("Structure")
    grid("dispatch").wait("Structure")

    log.info("Finished Structures!")

class Structure:
    pass

class Room:
    pass

class Building:
    pass

class GenStructure:
    def __init__(self, data):
        self.zone, self.random = data

class GenRoom:
    def __new__(cls, *args, **kwargs):
        if cls == GenRoom:
            msg = "Base Class: '{}' Can Not Be Instantiated!".format(cls.__name__)
            log.critical(msg)
            raise TypeError(msg)

    def __init__(self):
        pass

class RoomType:
    class InitRoom(GenRoom):
        def __init__(self):
            super().__init__()
