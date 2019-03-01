import libs
import iofile
from vector import Vector
from src import logic, visual, network

class Game:

    def __init__(self):
        self.options = iofile.read.cfg("options")
        self.lb = logic.Board()
        self.lb.build()
        self.vc = visual.Control(self)
        self.ns = network.Server(self, True)
        self.nc = network.Client(self, True)

    def __repr__(self):
        return "{}\n{}\n{}".format(self.lb, self.vc, "nc")

    def update_options(*args):
        global options
        options = iofile.read.cfg("options")
        for i in args:
            getattr(self, i).update_options()

#---Events---------------------------------------------------------------------#

    def select(self, pos):
        val = self.lb.select(pos)
        self.vc.vb.select(pos, val)
        if val == 1:
            pass # do network stuff

    def get_players(self):
        return self.nc.get_players()

#---Run------------------------------------------------------------------------#

main_game = Game()
main_game.vc.mainloop()
