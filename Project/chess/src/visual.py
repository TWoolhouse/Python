import libs
import gui
import graphics
from vector import Vector

#---Global Variables-----------------------------------------------------------#

characters = [{"Pawn":"♟", "Knight":"♞", "Bishop":"♝", "Rook":"♜", "Queen":"♛", "King":"♚"}, {"Pawn":"♙", "Knight":"♘", "Bishop":"♗", "Rook":"♖", "Queen":"♕", "King":"♔"}]

scale = 80
pallet = [(0, 0, 0), (255, 255, 255)] # allows for dynamically changing the colour of the game

#---Classes--------------------------------------------------------------------#

class Control(gui.Window):

    def __init__(self, main):
        self.main = main
        super().__init__("Chess Control")
        self.update_options()

        self.vb = Board(self)
        self.vb.close()

        PageMenu(self, "menu")
        PageGame(self, "game")
        PageNetwork(self, "network")
        PagePlayers(self, "players")
        PageOptions(self, "options")
        self.show_page("menu")

    def update_options(self):
        global scale
        global pallet
        scale = self.main.options["visual"]["scale"]
        pallet = [tuple((int(j) for j in self.main.options["visual"][i].split(", "))) for i in ("black", "white")]

class Board:

    def __init__(self, parent):
        self.parent = parent
        self.parent.vb_open = True
        self.gbs = graphics.Screen("Chess Board") # the screen the board is on
        self.gbs.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", self.close)
        self.gbts = graphics.Turtle() # graphics board turtle squares
        self.gbtp = graphics.Turtle() # graphics board turtle pieces
        self.gbth = graphics.Turtle() # graphics board turtle highlight
        self.gbs.onclick(self.click)
        self.gbs.onclick(self.clear_selected, btn=3)

    def close(self):
        self.parent.vb_open = False
        self.gbs.bye()
        self.parent.focus_force()

    def click(self, x, y):
        pos = Vector(x, y)
        pos -= pos % scale
        pos = Vector(*(int(a) for a in (pos-Vector(-4*scale, -4*scale))/scale))
        if (-1 < pos[0] < 8) and (-1 < pos[1] < 8):
            self.parent.main.select(pos)

    def select(self, pos, val):
        self.gbth.clear()
        if val == 1:
            self.draw_pieces()
        elif val == 2:
            self.draw_moves(self.parent.main.lb.grid[pos].piece)
            self.draw_highlight(self.parent.main.lb.grid[pos], "green", 2)
        elif val == 3:
            self.draw_moves(self.parent.main.lb.grid[pos].piece)
            self.draw_highlight(self.parent.main.lb.grid[pos], "red", 2)

    def draw_board(self):
        self.gbts.clear()
        for col in self.parent.main.lb.grid:
            for row in col:
                self.gbts.goto(Vector(-4*scale, -4*scale)+row.pos*scale) #goes to bottom left of square pos

                colour = row.colour*200 # sets the colour based on the piece
                self.gbts.color(colour+50, colour+50, colour+50)

                # draws the square
                self.gbts.begin_fill()
                for i in range(4):
                    self.gbts.fd(scale)
                    self.gbts.rt(90)
                self.gbts.end_fill()

    def draw_pieces(self):
        self.gbtp.clear()
        for col in self.parent.main.lb.grid:
            for row in col:
                if row.piece != None:
                    self.gbtp.goto((Vector(-4*scale, -4*scale)+row.pos*scale)+Vector(scale/2, -int(scale*0.15))) # moves to bottom center of square
                    #self.gbtp.color(pallet[row.piece.colour]) # change piece colours
                    self.gbtp.write(characters[row.piece.colour][type(row.piece).__name__], align="center", font=("Arial", int(scale*0.8), "normal"))

    def draw_highlight(self, space, colour="black", width=1):
        self.gbth.width(width)
        self.gbth.color(colour)
        self.gbth.goto((Vector(-4*scale, -4*scale)+space.pos*scale)+Vector(scale*0.05, scale*0.05))
        self.gbth.pd()
        for i in range(4):
            self.gbth.fd(scale*0.9)
            self.gbth.rt(90)
        self.gbth.pu()
        self.gbth.width(1)

    def draw_moves(self, piece):
        for space in piece.check_moves():
            colour = (pallet[not space.colour] if space.piece == None else "red")
            self.draw_highlight(space, colour, 2)

    def clear_selected(self, *args):
        self.parent.main.lb.selected = None
        self.gbth.clear()

#---Pages----------------------------------------------------------------------#

class PageMenu(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Label(self, text="Welcome to Chess"), row=0, column=0, columnspan=3, pady=15, sticky="ew")
        self.add(gui.tk.Button(self, text="Game", command=lambda: self.show_page("game")), pady=5)
        self.add(gui.tk.Button(self, text="Network", command=lambda: self.show_page("network")), pady=5)
        self.add(gui.tk.Button(self, text="Options", command=lambda: self.show_page("options")), pady=5)

class PageGame(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Button(self, text="Menu", command=lambda: self.show_page("menu")), row=0, column=0, columnspan=3, pady=15, sticky="ew")
        self.add(gui.tk.Button(self, text="Board", command=self.play))
        self.add(gui.tk.Button(self, text="Save", command=WIP))
        self.add(gui.tk.Button(self, text="Load", command=WIP))
        self.add(gui.tk.Button(self, text="Leave", command=WIP))

    def play(self):
        if not self.parent.vb_open:
            self.parent.vb = Board(self.parent)
        self.parent.vb.gbs.listen()
        self.parent.vb.draw_board()
        self.parent.vb.draw_pieces()

class PageNetwork(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Button(self, text="Menu", command=lambda: self.show_page("menu")), row=0, column=0, columnspan=3, pady=15, sticky="ew")
        if self.parent.main.options["network"]["allowed"]:
            self.add(gui.tk.Button(self, text="Join", command=lambda: self.show_page("players")))
            self.add(gui.tk.Button(self, text="Leave", command=WIP))
        else:
            self.add(gui.tk.Text(self, text="Networking is Disabled"))

    def join(self, id):
        print(id)
        if self.parent.main.set_target(id[0]):
            print("RELAY GOOD")
            self.show_page("network")
        else:
            print("RELAY FAIL")
            self.show_page("players")

    def leave(self):
        pass

class PagePlayers(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Button(self, text="Menu", command=lambda: self.show_page("menu")), row=0, column=0, pady=15, sticky="ew")
        self.add(gui.tk.Button(self, text="Avalible Players: 0", command=lambda: self.show()), name="active", row=1, column=0, pady=5, sticky="ew")
        self.p = 0

    def show(self):
        for i in range(self.p):
            self.wigets[i].delete()
            del self.wigets[i]
        players = self.parent.main.get_players()
        for k,i in enumerate(players):
            self.add(gui.tk.Button(self, text=i[1], command=gui.Cmd(self.parent["network"].join, i)), name=k, row=2+k, column=0)
        self.edit("active", "text", "Avalible Players: "+str(len(players)))

class PageOptions(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Button(self, text="Menu", command=lambda: self.show_page("menu")), row=0, column=0, columnspan=3, pady=15, sticky="ew")

#---Functions------------------------------------------------------------------#

def WIP():
    print("THIS BUTTON IS A PLACEHOLDER")

#---Setup----------------------------------------------------------------------#

#---Main Loop------------------------------------------------------------------#

#---End------------------------------------------------------------------------#
