import enum

_states = dict()

class State:
    def __new__(cls, key, value=None):
        if value == None:
            if isinstance(key, type):
                return _states[key]
            else:
                return _states[type(key)] == key
        else:
            if key in _states and isinstance(value, key):
                _states[key] = value
                return None
            else:
                raise TypeError("'{}' is not of type '{}'".format(value.__class__.__name__, key.__qualname__))
        raise TypeError("'{}' can not be instantiated!".format(cls))

    @enum.unique
    class Game(enum.Enum):
        Null = 0
        Quit = 1
        Menu = 2
        Chess = 3

    @enum.unique
    class TurtleWindow(enum.Enum):
        Null = 0
        Open = 1
        Closed = 2

    @enum.unique
    class Board(enum.Enum):
        Null = 0
        Active = 1
        Closed = 2
        Check = 3
        Checkmate = 4

for key, value in State.__dict__.items():
    if not key.startswith("_") and isinstance(value, type) and issubclass(value, enum.Enum):
        _states[value] = value(0)
