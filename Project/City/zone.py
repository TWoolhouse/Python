import config as cfg
from log import log

import libs
from vector import Vector

ORIENTATION = (Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0))

def generate(grid):
    log.info("Generating Zones")

    grid.data["zones"] = 1
    grid.add("zone", False)

    for gy in range(grid("height")):
        for gx in range(grid("width")):
            gcell = grid[gx, gy]
            zone = calc_zone(grid, gcell, gx, gy)
            if len(zone) > 0:
                grid.data["zones"] += 1

    log.info("Finished Zones!")

def calc_zone(grid, gcell, gx, gy):
    if type(gcell["road"]).__name__ == "Gap" and gcell["zone"] == False:
        chosen = set()
        target = [Vector(gx, gy)]
        count = 0
        while count < len(target):
            pos = target[count]
            for vec in ORIENTATION:
                nos = pos + vec
                cell = grid[nos]
                if nos[0] >= 0 and nos[0] < grid("width") and nos[1] >= 0 and nos[1] < grid("height") and nos not in chosen and cell["zone"] != False:
                    target.append(nos)
                    chosen.add(nos)
            grid[pos]["zone"] = grid("zones")
    return zone
