import config as cfg
import logging

cfg.load()
cfg.load("log")

filename = "{}/{}".format(cfg.general.info["output"], cfg.log.info["output"])
level = getattr(logging, cfg.log.info["level"].upper())

logger = logging.getLogger("City")

format = logging.Formatter("[{asctime}>{levelname}] {module}.{funcName} -> {message}", datefmt="%H:%M:%S", style="{")
handler = logging.FileHandler(filename, mode="w")

logger.setLevel(level)
handler.setFormatter(format)
logger.addHandler(handler)
