import libs
import node
import sound
import time

vol = sound.Volume(15)
media = sound.Media()

def volume(self, volume, rel):
    try:
        print("Volume:", vol.set_volume(int(volume), True if rel == "True" else False))
        self.send(vol.volume(), "vol")
    except ValueError:  pass
def prev(self):
    media.prev()
    print("Previous")
def next(self):
    media.next()
    print("Next")
def pause(self):
    media.pause()
    print("Play/Pause")

host = node.Server(funcs={"volume":volume, "pause":pause, "next":next, "prev":prev})
host.open()
while host:
    if input():
        break
host.close()
