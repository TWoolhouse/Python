import libs
import server
import client
import iofile

#---Global Variables-----------------------------------------------------------#

#---Classes--------------------------------------------------------------------#

class Server():

    def __init__(self, parent, open=False):
        self.parent = parent
        self.network = server.Server("", parent.options["network"]["port"], parent.options["network"]["max_conns"], **{"PLAYERS":self.get_players})
        if open:
            self.open()

    def update_options(self):
        self.network.port, self.network.limit = self.parent.options["network"]["port"], self.parent.options["network"]["max_conns"]
        self.network.close()
        self.open()

    def open(self):
        if self.parent.options["network"]["allowed"] and self.parent.options["network"]["host"]:
            self.network.open()

    def get_players(self, s, *args):
        s.send("|^|".join([str(i)+"|NAME" for i in s.server.connections]), "PLAYERS")

class Client():

    def __init__(self, parent, open=False):
        self.parent = parent
        self.network = client.Client(parent.options["network"]["address"], parent.options["network"]["port"])
        if open:
            self.open()

    def update_options(self):
        self.network.addr, self.network.port = self.parent.options["network"]["address"], self.parent.options["network"]["port"]
        self.network.close()
        self.open()

    def open(self):
        if self.parent.options["network"]["allowed"]:
            self.network.open()

    def get_players(self):
        self.network.send("get_players", "PLAYERS")
        return [j for j in [i.split("|") for i in self.network.data("PLAYERS")[0][1].split("|^|")] if j[0] != str(self.network.id)]

#---Functions------------------------------------------------------------------#

#---Setup----------------------------------------------------------------------#

#---Main Loop------------------------------------------------------------------#

#---End------------------------------------------------------------------------#
