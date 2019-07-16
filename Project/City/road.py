import config as cfg
from log import log, logfunc

import libs
import iofile
from vector import Vector

cfg.load("road")

ORIENTATION = [Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)] # N,E,S,W

# Failstates:
# 0 - None
# 1 - Offmap
# 2 - Road Collision - Road
# 3 - Road Collision - Gap
# 4 - Gap Collision

def generate(grid):
    log.info("Generating Road Grid")
    grid("random").load()
    Layout(grid)
    log.info("Finished Road Grid!")
    return grid

class Cell:
    def __init__(self):
        pass

class Road(Cell):
    def __init__(self, name, orientation, location):
        self.name = name
        self.orientation = orientation
        self.location = location
        self.children = []

class Intersection(Road):
    def __init__(self, *roads):
        pass

class Gap(Cell):
    def __init__(self, orientation, parent):
        self.orientations = [orientation]
        self.parents = [parent]

class Layout:
    def __init__(self, grid):
        self.grid = grid
        self.grid.add("road", Cell())
        self.load_templates()
        self.generate()

    def load_templates(self):
            self.roads = {}
            for f in cfg.road.roads.values():
                file = iofile.read.json("Road/"+f)
                for i in file:
                    self.roads[f+"."+i] = file[i]
            log.debug("Loaded Road Templates: {}\n\t{}".format(len(self.roads), "\n\t".join(("{} -> Priority:{p}, Chance:{c}%, Width:{w}, Length:{l1}-{l2}, Gap:{g1}-{g2}".format(k, p=v["priority"], c=v["chance"]*100, w=v["width"], l1=v["length"][0], l2=v["length"][1], g1=v["gap"][0], g2=v["gap"][1]) for k,v in self.roads.items()))))
            return self.roads

    def generate(self):
        for pos in distribution(self.grid):
            GenRoad(pos, self)
        log.debug("Layout: %d/%d Road Pieces", sum([1 for i in self.grid.all() if isinstance(i["road"], Road)]), cfg.general.map["width"]*cfg.general.map["height"])

class Orientation:
    def __init__(self, index):
        self.north = index
        self.east = (index + 1) % 4
        self.south = (index + 2) % 4
        self.west = (index + 3) % 4
        self.north_vec = ORIENTATION[self.north]
        self.east_vec = ORIENTATION[self.east]
        self.south_vec = ORIENTATION[self.south]
        self.west_vec = ORIENTATION[self.west]

class GenRoad:
    def __init__(self, pos, parent):
        self.parent = parent
        for ori in self.parent.grid("random").sample([0, 1, 2, 3], 4):
            self.failstate = 0
            if self.setup() == False:
                break
            self.orientation = Orientation(ori)
            if self.main(pos):
                if self.validate():
                    self.update()
                    return None

    def main(self, pos):
        self.segments = []
        for length in range(self.road["length"][1]):
            for width in range(self.road["width"]):
                seg = self.calc_seg(pos, length, width)
                if seg:
                    self.segments.append(seg)
                else:
                    return False
        return True

    def calc_seg(self, pos, length, width):
        cell = pos + (self.orientation.north_vec * length) + (self.orientation.east_vec * width)
        if self.offmap(cell) or self.valid_road(cell):
            return False
        seg = [(cell, self.orientation.north, width), []]
        if width == 0:
            res = self.calc_gaps(cell, self.orientation.west_vec, self.orientation.west, self.orientation.east)
            if res != False:
                seg[1].extend(res)
            else:   return False
        if width == self.road["width"] - 1:
            res = self.calc_gaps(cell, self.orientation.east_vec, self.orientation.east, self.orientation.west)
            if res != False:
                seg[1].extend(res)
            else:   return False
        return seg

    def calc_gaps(self, pos, vec, ori, iori):
        gs = []
        for g in range(1, self.settings["gap"] + 1):
            gp = pos + vec * g
            if self.offmap(gp):
                continue
            cell = self.parent.grid[gp]["road"]
            if isinstance(cell, Road):
                if cell.orientation in (ori, iori):
                    continue
                else:
                    self.failstate = 3
                    return False
            if isinstance(cell, Gap):
                if len(cell.orientations) < 2:
                    if iori in cell.orientations or ori in cell.orientations:
                        self.failstate = 4
                        return False
                else:
                    self.failstate = 4
                    return False
            gs.append((gp, ori))
        return gs

    def setup(self):
        choices = sorted([{**self.parent.roads[i], "name":i} for i in self.parent.roads if self.parent.grid("random").random() <= self.parent.roads[i]["chance"]], key=lambda x: x["priority"])
        if not choices:
            return False # No road avalible to use
        priority = choices[0]["priority"]
        self.road = self.parent.grid("random").choice([i for i in choices if i["priority"] == priority])
        self.gen_settings()

    def gen_settings(self):
        self.settings = {
            "length":self.parent.grid("random").randint(*self.road["length"]),
            "gap":self.parent.grid("random").randint(*self.road["gap"]),
        }

    def offmap(self, pos):
        if pos[0] < 0 or pos[0] >= self.parent.grid("width") or pos[1] < 0 or pos[1] >= self.parent.grid("height"):
            return True
        return False

    def valid_road(self, pos):
        cell = self.parent.grid[pos]["road"]
        if isinstance(cell, Road):
            self.failstate = 2
            return True
        if isinstance(cell, Gap):
            if len(cell.orientations) > 1:
                self.failstate = 3
                return True
            elif self.orientation.north in cell.orientations or self.orientation.south in cell.orientations:
                return False
        return False

    def validate(self):
        if len(self.segments) % self.road["width"]:
            self.segments = self.segments[:len(self.segments) // self.road["width"] * self.road["width"]]
        if self.failstate != 0 and len(self.segments) > self.settings["length"] * self.road["width"]:
            self.segments = self.segments[:self.settings["length"] * self.road["width"]]
        if len(self.segments) // self.road["width"] >= self.road["length"][0]:
            return True
        return False

    def update(self):
        for road, gaps in self.segments:
            parent = Road(self.road["name"], *road[1:])
            self.parent.grid[road[0]]["road"] = parent
            for gap, ori in gaps:
                cell = self.parent.grid[gap]["road"]
                if isinstance(cell, Gap):
                    cell.orientations.append(ori)
                    cell.parents.append(parent)
                    parent.children.append(cell)
                else:
                    child = Gap(ori, parent)
                    self.parent.grid[gap]["road"] = child
                    parent.children.append(child)

def distribution(grid):
    log.debug("Distribution: {}".format(cfg.road.info["distro"].title()))
    return getattr(Distribution, "d_"+cfg.road.info["distro"].replace(" ", "_").lower())(grid)

class Distribution:
    def d_scan(*args):
        for y in range(cfg.general.map["height"]):
            for x in range(cfg.general.map["width"]):
                yield Vector(x, y)

    def d_scan_flip(*args):
        for x in range(cfg.general.map["width"]):
            for y in range(cfg.general.map["height"]):
                yield Vector(x, y)

    def d_spiral(*args):
        cx = cfg.general.map["width"] // 2
        cy = cfg.general.map["height"] // 2

        count = 1
        pos = Vector(cx, cy)
        orientation = Vector(0, 1)

        while True:
            for i in range(2):
                nos = pos
                for r in range(1, count + 1):
                    nos = pos + orientation * r
                    x = False
                    y = False
                    if nos[0] >= 0 and nos[0] < cfg.general.map["width"]:
                        x = True
                    if nos[1] >= 0 and nos[1] < cfg.general.map["height"]:
                        y = True
                    if x and y:
                        yield nos
                    if not x and not y:
                        return
                orientation = Vector(*map(int, orientation.rotate(90)))
                pos = nos
            count += 1

    def d_sprawl(*args):
        cx = cfg.general.map["width"] // 2
        cy = cfg.general.map["height"] // 2
        size = cfg.general.map["width"] * cfg.general.map["height"]
        width = cfg.general.map["width"]
        height = cfg.general.map["height"]

        chosen = set()
        target = [Vector(cx, cy)]

        count = 0
        while count < size:
            pos = target[count]
            for vec in ORIENTATION:
                nos = pos + vec
                nos_h = tuple(nos)
                if nos[0] >= 0 and nos[0] < width and nos[1] >= 0 and nos[1] < height and nos_h not in chosen:
                    target.append(nos)
                    chosen.add(nos_h)
            yield pos
            count += 1

    def d_random(grid):
        random = grid("random")
        chosen = set()
        size = cfg.general.map["width"] * cfg.general.map["height"]
        width = cfg.general.map["width"] - 1
        height = cfg.general.map["height"] - 1

        while len(chosen) < size:
            x = random.randint(0, width)
            y = random.randint(0, height)

            if (x,y) not in chosen:
                chosen.add((x,y))
                yield Vector(x, y)
