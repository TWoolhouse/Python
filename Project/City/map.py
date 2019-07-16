import config as cfg
from log import log
from Source import noise_map

cfg.load("map")

def generate(grid):
    log.info("Generating Map")
    grid("random").load()
    grid("dispatch").new("Map", value=grid, output=True)
    grid("dispatch")["Map"] = terrain
    grid("dispatch")["Map"] = wealth
    grid("dispatch")["Map"] = tech

    grid("dispatch")("Map")
    grid("dispatch").wait("Map")
    n_maps = dict(grid("dispatch")["Map"])
    for x in range(grid("width")):
        for y in range(grid("height")):
            grid[x][y].add("map", grid.node(terrain=n_maps["terrain"][x][y], wealth=n_maps["wealth"][x][y], tech=n_maps["tech"][x][y]))

    log.info("Finished Map!")
    return grid

def terrain(grid):
    log.info("Generating Terrain Map")
    terrain = noise_map.generate(cfg.general.map["width"], cfg.general.map["height"], cfg.map.terrain["min"], cfg.map.terrain["max"], cfg.map.terrain["min"], "Map/"+cfg.map.layers["terrain"], grid("random"), grid("noise"), grid("seed"), grid("dispatch"))
    log.info("Finished Terrain Map!")
    return "terrain", terrain

def wealth(grid):
    log.info("Generating Wealth Map")
    wealth = noise_map.generate(cfg.general.map["width"], cfg.general.map["height"], cfg.map.wealth["min"], cfg.map.wealth["max"], cfg.map.wealth["base"], "Map/"+cfg.map.layers["wealth"], grid("random"), grid("noise"), grid("seed"), grid("dispatch"))
    log.info("Finished Wealth Map!")
    return "wealth", wealth

def tech(grid):
    log.info("Generating Tech Map")
    tech = noise_map.generate(cfg.general.map["width"], cfg.general.map["height"], cfg.map.tech["min"], cfg.map.tech["max"], cfg.map.tech["base"], "Map/"+cfg.map.layers["tech"], grid("random"), grid("noise"), grid("seed"), grid("dispatch"))
    log.info("Finished Tech Map!")
    return "tech", tech
