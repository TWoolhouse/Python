from Source import setup
import config as cfg
from log import log
import threading
import queue

import map
import road
import zone

import libs
import randstate
import noise as _noise
import iofile
from grid import Grid
from vector import Vector

#---Global Variables-----------------------------------------------------------#

#---Classes--------------------------------------------------------------------#

class Grid(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node = kwargs["val"]
        self.data = {
            "dispatch":Dispatcher(cfg.general.info["threads"]),
            "width":args[0], "height": args[1],
        }

    def __call__(self, key):
        return self.data[key]
    def add(self, name, val, *args, **kwargs):
        if isinstance(val, type):
            for i in self.all():
                i.data[name] = val(*args, **kwargs)
        else:
            for i in self.all():
                i.data[name] = val

class Node:

    def __init__(self, **kwargs):
        self.data = kwargs

    def __str__(self):
        return self.data.__str__()
    def __repr__(self):
        return self.data.__repr__()

    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def add(self, name, val):
        self.data[name] = val

class Dispatcher:
    def __init__(self, num=1):
        self.workers = {threading.Thread(target=self.dispatch) for i in range(num)}
        self.running = threading.Event()
        self.event = threading.Event()
        self.queue = queue.Queue()
        self.active = None
        self.data = {}
        self.output = {}

        self.new(self.active)

        self.running.set()
        for w in self.workers:
            w.start()

    def __call__(self, key):
        self.queue.put(key)
        if not self.event.is_set():
            self.next()

    def __getitem__(self, key):
        queue = self.output[key]
        try:
            for i in range(queue.qsize()):
                r = queue.get()
                queue.task_done()
                yield r
        except queue.Empty: return

    def __setitem__(self, key, data):
        self.data[key][0].put(data)

    def new(self, key, func=None, value=None, output=False):
        self.data[key] = (queue.Queue(), func, value, output)
        if output:
            self.output[key] = queue.Queue()

    def next(self):
        self.event.clear()
        try:
            key = self.queue.get_nowait()
            self.active = key
            self.queue.task_done()
            self.event.set()
        except queue.Empty: pass

    def dispatch(self):
        while self.running.is_set():
            self.event.wait()
            que, func, value, is_output = self.data[self.active]
            try:
                if value:
                    if func:
                        if is_output:
                            output = self.output[self.active]
                            while True:
                                item = que.get_nowait()
                                r = func(value, item)
                                que.task_done()
                                output.put(r)
                        else:
                            while True:
                                item = que.get_nowait()
                                func(value, item)
                                que.task_done()
                    else:
                        if is_output:
                            output = self.output[self.active]
                            while True:
                                item = que.get_nowait()
                                r = item(value)
                                que.task_done()
                                output.put(r)
                        else:
                            while True:
                                item = que.get_nowait()
                                item(value)
                                que.task_done()
                else:
                    if func:
                        if is_output:
                            output = self.output[self.active]
                            while True:
                                item = que.get_nowait()
                                r = func(item)
                                que.task_done()
                                output.put(r)
                        else:
                            while True:
                                item = que.get_nowait()
                                func(item)
                                que.task_done()
                    else:
                        if is_output:
                            output = self.output[self.active]
                            while True:
                                item = que.get_nowait()
                                r = item()
                                que.task_done()
                                output.put(r)
                        else:
                            while True:
                                item = que.get_nowait()
                                item()
                                que.task_done()
            except queue.Empty:
                if not self.event.is_set():
                    continue
                self.next()

    def wait(self, key):
        self.data[key][0].join()

    def stop(self):
        self.running.clear()
        self.event.set()

#---Functions------------------------------------------------------------------#

#---Setup----------------------------------------------------------------------#

grid = Grid(cfg.general.map["width"], cfg.general.map["height"], val=Node)

grid.data["seed"] = cfg.general.info["seed"] = cfg.general.info["seed"] if isinstance(cfg.general.info["seed"], int) else sum((int(i) if i.isdigit() else ord(i) for i in str(cfg.general.info["seed"])))

grid.data["random"] = randstate.Random(cfg.general.info["seed"])
grid.data["noise"] = _noise.SimplexNoise()

grid("random").save()

log.info("Generating City:\n\tSeed: {}\n\tWidth: {}\n\tHeight: {}\n\tCells: {}\n\tThreads: {}".format(
grid("seed"),
grid("width"), grid("height"), grid("width") * grid("height"),
cfg.general.info["threads"]
))

#---Main Loop------------------------------------------------------------------#

# map.generate(grid)
road.generate(grid)
zone.generate(grid)

export = {**grid.data, "data":[(Vector(x, y), grid[x, y]) for x in range(grid("width")) for y in range(grid("height"))]}

# iofile.write.pickle("Output/output", export, ext="raw")
# Export Full Grid
# iofile.write.pickle("Output/output", grid, ext="raw")

#---End------------------------------------------------------------------------#

grid("dispatch").stop()
log.info("Finished City!")

# quit()
from Source import vis_rep
vis_rep.main(export, "road", "zone")
vis_rep.loop()
