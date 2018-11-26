import libs
import server
import client
import iofile

#---Global Variables-----------------------------------------------------------#

options = {}

#---Classes--------------------------------------------------------------------#

class Server(server.Server):

    def __init__(self):
        super().__init__("", options["port"], options["max_conns"], commands="src.commands")
        if options["allowed"]:
            self.open()

    def update_options(self):
        set_options()
        self.port, self.limit = options["port"], options["max_conns"]

class Client(client.Client):

    def __init__(self):
        super().__init__(options["address"], options["port"])
        if options["allowed"]:
            self.open()

    def update_options(self):
        set_options()
        self.addr, self.port = options["address"], options["port"]

    def save_req(self, name, data):
        self.cmd("save", name)
        self.send(data, bin=True)
        if self.recv() == "FILE":
            return True
        return False

    def load_req(self, name):
        self.cmd("load", name)
        data = self.recv(size=8192, bin=True)
        if data != b"NO FILE":
            return iofile.pickle.loads(data)
        return False

    def transfer_req(self, data):
        if self.save_req("temp/"+str(self.id), data):
            return self.cmd("recv_turn", self.id, slv=True)
        return False

    def recv_turn(self, name):
        data = self.load_req("temp/"+str(name))
        if data:
            iofile.write

#---Functions------------------------------------------------------------------#

def set_options():
    global options
    options = iofile.read.cfg("options")["network"]

#---Setup----------------------------------------------------------------------#

set_options()

#---Main Loop------------------------------------------------------------------#

#---End------------------------------------------------------------------------#
