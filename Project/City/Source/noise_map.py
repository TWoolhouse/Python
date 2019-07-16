from log import log

import libs
import iofile

def generate(width, height, val_min, val_max, val_base, layers_name, random, noise, seed, dispatch):
    layers = [i for i in iofile.read.json(layers_name)]

    log.debug("Generating Noise Map:\n\tWidth: {}\n\tHeight: {}\n\tLayers: {}\n\tNumber of Layers: {}\n\tMin Height: {}\n\tMax Height: {}\n\tBase Height: {}".format(
        width, height, layers_name, len([i for i in layers if i["enabled"]]), val_min, val_max, val_base))

    grid, largest = gen(width, height, layers, random, noise, seed)

    log.debug("Finished Noise Map!")
    log.debug("Adjusting Map")

    grid = adjust(width, height, val_min, val_max, val_base, grid, largest)

    log.debug("Finished Noise Map!")
    return grid

def gen(width, height, layers, random, noise, seed):

    x_off = seed * (1000 if random.randint(0, 1) else -1000) + random.randint(1000, 10000)
    y_off = seed * (1000 if random.randint(0, 1) else -1000) + random.randint(1000, 10000) + 1000

    grid = []
    largest = 0
    for x in range(width):
        col = []
        for y in range(height):

            x += x_off
            y += y_off

            elev = elevation(x, y, layers, noise)

            col.append(elev)
        grid.append(col)
        largest = max(largest, *col)

    return grid, largest

def elevation(x, y, layers, noise):

    first_layer = 0
    elev = 0

    if len(layers) > 0:
        first_layer = evaluate(x, y, layers[0], noise)
        if layers[0]["enabled"]:
            elev += first_layer

    for l in layers[1:]:
        if l["enabled"]:
            mask = first_layer if l["mask"] else 1
            elev += evaluate(x, y, l, noise) * mask

    return elev

def evaluate(x, y, layer, noise):
    value = 0
    frequency = layer["base_roughness"]
    amplitude = 1

    for i in range(layer["num_layers"]):
        v = noise.noise2(x * frequency, y * frequency)
        value += (v + 1) * .5  * amplitude
        frequency *= layer["roughness"]
        amplitude *= layer["persistence"]

    value = max(0, value - layer["min_value"])
    return value * layer["strength"]

def adjust(width, height, val_min, val_max, val_base, grid, largest):
    for x in range(width):
        for y in range(height):
            grid[x][y] = max(val_base, (grid[x][y] / largest * (val_max - val_min) + val_min))
    return grid
