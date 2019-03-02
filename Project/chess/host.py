import libs
import server

class Server():

    def __init__(self, parent, open=False):
        self.parent = parent
        #self.network = server.Server("", parent.options["network"]["port"], parent.options["network"]["max_conns"], **{"PLAYERS":self.get_players})
        self.network = server.Server("", 80, 10, **{"PLAYERS":get_players})
        if open:
            self.open()

    # def update_options(self):
    #     self.network.port, self.network.limit = self.parent.options["network"]["port"], self.parent.options["network"]["max_conns"]
    #     self.network.close()
    #     self.open()

    def open(self):
        # if self.parent.options["network"]["allowed"] and self.parent.options["network"]["host"]:
        self.network.open()

def get_players(s, *args):
    s.send("|^|".join([str(i)+"|NAME" for i in s.server.connections]), "PLAYERS")

ns = Server(True, True)
input()
