import libs
import node
import time

class Phone(node.Client):
    def volume(self, vol=0, rel=False):
        self.cmd("volume", vol, rel)
    def prev(self):
        self.cmd("prev")
    def next(self):
        self.cmd("next")
    def pause(self):
        self.cmd("pause")

volume = None

def set_volume(self, vol):
    global volume
    volume = vol[1]

p = Phone("127.0.0.1", callbacks={"vol":set_volume})
p.open()
while True:
    i = input("\n(V)olume - "+str(volume)+", (P)ause, Prev, Next:\n").lower()
    if i[0] == "v":
        p.volume(*i.replace("t", "True").split(" ")[1:])
        time.sleep(0.1)
    elif i == "prev":
        p.prev()
    elif i == "next":
        p.next()
    elif i == "p":
        p.pause()
    elif i == "quit":
        break
    else:
        print("NOT VALID COMMAND")

p.close()
