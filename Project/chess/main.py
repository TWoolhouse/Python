import libs
import iofile
from vector import Vector
from src import logic, visual, network

class Game:

    def __init__(self):
        self.up = False
        self.options = iofile.read.cfg("options")
        self.lb = logic.Board()
        self.lb.build()
        self.vc = visual.Control(self)
        #self.ns = network.Server(self, True)
        self.nc = network.Client(self, True)

    def __repr__(self):
        return "{}\n{}\n{}".format(self.lb, self.vc, "nc")

    def update(self):
        self.up = True

    def update_options(*args):
        global options
        options = iofile.read.cfg("options")
        for i in args:
            getattr(self, i).update_options()

#---Events---------------------------------------------------------------------#

    def select(self, pos):
        val = self.lb.select(pos)
        self.vc.vb.select(pos, val)
        if val == 1 and self.nc.network.target != -1:
            self.save_board()
            self.nc.send_board(self.read_board())

    def get_players(self):
        return self.nc.get_players()

    def set_target(self, id):
        return self.nc.set_target(id)

#---Functions------------------------------------------------------------------#

    def save_board(self, file_name="_temp"):
        iofile.write.pickle("saves/"+file_name, self.lb)
    def load_board(self, file_name="_temp"):
        self.lb = iofile.read.pickle("saves/"+file_name)
    def read_board(self, file_name="_temp"):
        return iofile.read.bin("saves/"+file_name)
    def write_board(self, data, file_name="_temp"):
        iofile.write.bin("saves/"+file_name, data)

#---Run------------------------------------------------------------------------#

main_game = Game()

while True:
    if main_game.up:
        main_game.up = False
        main_game.vc.vb.draw_pieces()
    main_game.vc.update()
