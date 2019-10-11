import enum

class Tag():
    tags = {}

    def __new__(cls, tag: str, value: int=None):
        t = cls.tags[tag]
        return t if value is None else t(value) if isinstance(value, int) else getattr(t, value)
    
    def __init__(self, tag: str, value: int = None):
        pass

    @classmethod
    def name(cls, tag):
        for name, obj in cls.tags.items():
            if isinstance(tag, obj) or obj is tag:
                return name

@enum.unique
class Sex(enum.IntEnum):
    Other = 0
    Male = 1
    Female = 2

for name, obj in list(globals().items()):
    if isinstance(obj, type) and issubclass(obj, enum.IntEnum):
        Tag.tags[name] = obj