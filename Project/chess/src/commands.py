import libs
import iofile

def save(self, name):
    try:
        iofile.write.bin("saves/server/"+name, self.recv(size=8192, bin=True), ext="sav")
        self.send("", prefix="PASS")
        self.send("FILE")
    except IOError:
        self.send("NO FILE")

def load(self, name):
    try:
        self.send("", prefix="PASS")
        self.send(iofile.read.bin("saves/server/"+name, ext="sav"), bin=True, prefix="PASS")
    except IOError:
        self.send("NO FILE")
