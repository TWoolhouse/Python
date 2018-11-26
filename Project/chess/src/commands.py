import libs
import iofile

def save(self, name):
    try:
        iofile.write.bin("saves/server/"+name, self.recv(size=8192, bin=True), ext="sav")
        self.send("", prefix="PASS")
        self.send("FILE")
        msg = "Save Sucessful"
    except IOError:
        self.send("NO FILE")
        msg = "Save Failed"
    print("{} [{}]: Saving {} - {}".format(self.id, self.addr, name, msg))

def load(self, name):
    try:
        self.send("", prefix="PASS")
        self.send(iofile.read.bin("saves/server/"+name, ext="sav"), bin=True, prefix="PASS")
        msg = "Load Sucessful"
    except IOError:
        self.send("NO FILE")
        msg = "Load Failed"
    print("{} [{}]: Loading {} - {}".format(self.id, self.addr, name, msg))
