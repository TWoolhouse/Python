import libs
import iofile

class Collection:
    def __init__(self, **cfg):
        self.cfg = cfg
        for c in cfg:
            setattr(self, c, cfg[c])

    def __iter__(self):
        return self.cfg.values().__iter__()

    def __len__(self):
        return len(self.cfg)

def load(file_name="general"):
    data = iofile.read.cfg("Settings/"+file_name)
    c = Collection(**data)
    globals()[file_name.split("/")[-1]] = c
