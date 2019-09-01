import config as cfg
from log import log

import libs
from vector import Vector

ORIENTATION = (Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0))

def generate(grid):
    log.info("Generating Zones")
    d_count = 0
    grid.add("zone", None)
    for x in range(grid("width")):
        for y in range(grid("height")):
            cell = grid[x, y]
            if cell["zone"] == None and type(cell["road"]).__name__ == "Gap":
                zone = Zone(cell["road"].orientation, d_count)
                calc_zone(grid, zone, Vector(x, y), cell["road"])
                zone.sort()
                d_count += 1
    log.debug("Zones Count: %d", d_count)
    log.info("Finished Zones!")

def calc_zone(grid, zone, pos, target):
    if pos[0] >= 0 and pos[0] < grid("width") and pos[1] >= 0 and pos[1] < grid("height"):
        cell = grid[pos]
        if not isinstance(cell["zone"], Zone) and type(cell["road"]).__name__ == "Gap" and cell["road"].orientation == target.orientation and cell["road"].parent.name == target.parent.name:
            if (target.parent.orientation in (0, 2) and target.parent.pos[0] == cell["road"].parent.pos[0]) or (target.parent.orientation in (1, 3) and target.parent.pos[1] == cell["road"].parent.pos[1]):
                zone.cells.append(cell)
                cell["zone"] = zone
                for vec in ORIENTATION:
                    calc_zone(grid, zone, pos + vec, target)

class Zone:
    def __init__(self, orientation, count):
        self.orientation = orientation
        self.cells = []
        self.width = 0
        self.height = 0
        self.count = count

    def sort(self):
        ori = self.orientation % 2
        cells = set(self.cells)
        rows = []
        for cell in self.cells:
            if cell in cells:
                col = []
                for c in set(cells):
                    if c.pos[ori] == cell.pos[ori]:
                        col.append(c)
                        cells.remove(c)
                target = ORIENTATION[self.orientation] * -len(col)
                col.sort(key=lambda x: x.pos.dist(target + x.pos, sqr=True))
                rows.append(col)
        self.height = max((len(col) for col in rows))
        for col in list(rows):
            if len(col) != self.height:
                rows.remove(col)
                for cell in col:
                    cell["zone"] = None
        self.width = len(rows)
        target = ORIENTATION[(self.orientation + 1) % 4] * -len(rows)
        rows.sort(key=lambda x:x[0].pos.dist(target + x[0].pos, sqr=True))
        self.cells = []
        for col in rows:
            self.cells.extend(col)
