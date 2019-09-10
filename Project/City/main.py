from Source import setup
import config as cfg
from log import log

import map
import road
import zone
import structure

import libs
import randstate
import noise as _noise
import iofile
from grid import Grid
from vector import Vector
import dispatch

#---Global Variables-----------------------------------------------------------#

#---Classes--------------------------------------------------------------------#

class Grid(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node = kwargs["val"]
        self.data = {
            "dispatch":dispatch.Dispatcher(cfg.general.info["threads"]),
            "width":args[0], "height": args[1],
        }
        for x in range(self.data["width"]):
            for y in range(self.data["height"]):
                self[x, y].pos = Vector(x, y)

    def __call__(self, key):
        return self.data[key]
    def add(self, name, val, *args, **kwargs):
        if isinstance(val, type):
            for i in self.all():
                i.data[name] = val(*args, **kwargs)
        else:
            for i in self.all():
                i.data[name] = val

    def locate(self, cell, data):
        for i in self.all():
            if i[cell] == data:
                return i

class Node:

    def __init__(self, **kwargs):
        self.data = kwargs
        self.pos = None

    def __str__(self):
        return "<{} {}>".format(self.pos.__str__(), self.data.__str__())
    def __repr__(self):
        return "<{} {}>".format(self.pos.__repr__(), self.data.__repr__())
    def __hash__(self):
        return hash(self.pos)

    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def add(self, name, val):
        self.data[name] = val

#---Functions------------------------------------------------------------------#

#---Setup----------------------------------------------------------------------#

grid = Grid(cfg.general.map["width"], cfg.general.map["height"], val=Node)

grid.data["seed"] = cfg.general.info["seed"] = cfg.general.info["seed"] if isinstance(cfg.general.info["seed"], int) else sum((int(i) if i.isdigit() else ord(i) for i in str(cfg.general.info["seed"])))

grid.data["random"] = randstate.Random(cfg.general.info["seed"])
grid.data["noise"] = _noise.SimplexNoise()

grid("random").save()

log.info("Generating City:\n\tSeed: %d\n\tWidth: %d\n\tHeight: %d\n\tCells: %d\n\tThreads: %d",
grid("seed"),
grid("width"), grid("height"), grid("width") * grid("height"),
cfg.general.info["threads"]
)

#---Main Loop------------------------------------------------------------------#

# map.generate(grid)
road.generate(grid)
zone.generate(grid)
structure.generate(grid)

export = {**grid.data, "data":[(Vector(x, y), grid[x, y]) for x in range(grid("width")) for y in range(grid("height"))]}

# iofile.write.pickle("Output/output", export, ext="raw")
# Export Full Grid
# iofile.write.pickle("Output/output", grid, ext="raw")

#---End------------------------------------------------------------------------#

grid("dispatch").stop()
log.info("Finished City!")

# quit()

# from Source import vis_rep
# vis_rep.main(export, "road", "zone", scale=2.5)
# vis_rep.loop()

# from Source import house_rep
# house_rep.main(export, "house")
# house_rep.loop()
