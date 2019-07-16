import config as cfg

import math
import libs
import util
import iofile
from vector import Vector
import randstate
import graphics

debug = cfg.general.info["debug"]
cfg.load("structure")
random = randstate.Random(10)

def convert_shapes(shapes):
    for shape in shapes:
        x, y = 0 ,0
        shape["verticies"] = [Vector(*p) for p in shape["verticies"]]
        for v in shape["verticies"]:
            x, y = max(x, v[0]), max(y, v[1])
        shape["corner"] = Vector(x+1, y+1)
    return shapes

def generate(width, height, cutoff, empty, random):
    area = width * height

    return calc_empty(area, empty, random)

def calc_empty(area, empty, random):
    shape = random.choice(empty_shapes)
    points = shape["verticies"]
    sf = int(math.sqrt((area * empty) / len(points)))
    points = enlarge(points, sf)
    points = transform(points, random)
    return shape

def enlarge(shape, scale):
    new_shape = []
    for p in shape:
        p = p * scale
        for x in range(scale):
            for y in range(scale):
                new_shape.append(p + Vector(x, y))
    return new_shape

def transform(shape, random):
    return shape

empty_shapes = convert_shapes(iofile.read.json("Settings/"+cfg.structure.shapes["empty"])["shapes"])

x = generate(10, 10, 1, 0.1, random)
print(x)

# gs = graphics.Screen("Test", (800, 800))
#
# polyominoes = [ # all as horizontal as possible
#     [(Vector(0,0),)], # 1
#     [(Vector(0,1),)], # 2
#     [   (Vector(0,0), Vector(1,0), Vector(2,0)), # 3
#         (Vector(0,0), Vector(1,0), Vector(0,1))],
# ]
#
# def generate(area, scale, random):
#     util.debug(debug, "Generate Structure:")
#     shapes = calc_polyominoes(area, scale)
#     shape = random.choice(shapes)
#     shape = transform(shape, random)
#     shape = enlarge(shape, scale)
#
#     return shape
#
# def calc_polyominoes(area, scale):
#     cell = scale ** 2
#     count = area // cell
#     print(count)
#     shapes = polyominoes[count-1]
#     return shapes
#
# shape = generate(30, 3, random)
#
# print(len(shape), shape)
#
# turtle = graphics.Turtle()
#
# for p in shape:
#     turtle.goto(p*10)
#     turtle.dot()
#
# gs.mainloop()
