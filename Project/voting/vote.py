import time

graph_size = 15
final_size = 3

def size(val=7):
    global graph_size
    graph_size = val

def pop(val=3):
    global final_size
    final_size = val

def vote(*args, **kwargs):
    return final(*args, **kwargs)

class Ballot(list):

    def __init__(self, *args):
        x = []
        for i in args:
            if not x.count(i):
                x.append(i)
        super().__init__(x)

    def vote_out(self, *items):
        for item in items:
            if item in self:
                self.remove(item)

def all_options(*blts):
    res = {}
    for b in blts:
        for v in b:
            res[v] = 0
    return res

def count(res, *blts):
    for b in blts:
        try:
            res[b[0]] += 1
        except IndexError:
            pass

def remove(res, *blts):
    lowest = sorted(res.values())[0]
    out = [k for k in res if res[k] == lowest]
    if not all((k in out for k in res)):
        for v in out:
            for b in blts:
                b.vote_out(v)
            del res[v]
        return True
    return False

def visual(res, scale=0, delay=0):
    highest, lowest = sorted(res.values())[-1], sorted(res.values())[0]
    if not scale:
        scale = (((highest-lowest)//graph_size) if (highest-lowest) > (graph_size*2) else 1)
    for y_val in range(highest, lowest-scale if lowest-scale > 0 else 0, -scale):
        time.sleep(delay)
        print(("{:>"+str(len(str(highest)))+"}: "+"".join("{:^"+str(len(str(topic)))+"} " for topic in sorted(res))).format(y_val, *(("|" if res[k] > (y_val-1) else " ") for k in sorted(res))))
    print(("{:>"+str(len(str(highest)))+"}+ "+"{} "*len(res)).format(scale, *sorted(res))+"\n")

def final(*blts, output=True, size=0, delay=0):
    for i in range(50):
        res = all_options(*blts)
        count(res, *blts)
        if output:
            visual(res, size, delay)
        if not remove(res, *blts):
            break
        if len(res) < final_size+1:
            break
    if output:
        visual(res, size, delay)
    return res
