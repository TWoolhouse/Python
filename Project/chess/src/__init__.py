import logging

filename = "{}.log".format("chess")
level = getattr(logging, "DEBUG".upper())

logger = logging.getLogger("Chess")

format = logging.Formatter("[{asctime}>{levelname}] {module}.{funcName} -> {message}", datefmt="%H:%M:%S", style="{")
handler = logging.FileHandler(filename, mode="w")

logger.setLevel(level)
handler.setFormatter(format)
logger.addHandler(handler)

logger.debug("Logger Initialized")
