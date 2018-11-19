import libs
import gui
import graphics
from vector import Vector
import iofile

#---Global Variables-----------------------------------------------------------#

characters = [{"Pawn":"♟", "Knight":"♞", "Bishop":"♝", "Rook":"♜", "Queen":"♛", "King":"♚"}, {"Pawn":"♙", "Knight":"♘", "Bishop":"♗", "Rook":"♖", "Queen":"♕", "King":"♔"}]

scale = 80
pallet = ["black", "white"] # allows for dynamically changing the colour of the game

#---Classes--------------------------------------------------------------------#

class Control(gui.Window):

    def __init__(self, board, client, server):
        super().__init__("Chess Control")

        self.lb = board
        self.nc = client
        self.ns = server

        PageGame(self, "game")
        PageNetwork(self, "network")
        PageChat(self, "chat")
        PageMenu(self, "menu")
        self.b_open = False

class Board:

    def __init__(self, parent, board):
        parent.b_open = True
        self.gbs = graphics.Screen("Chess Board") # the screen the board is on
        self.gbs.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", self.close)
        self.gbts = graphics.Turtle() # graphics board turtle squares
        self.gbtp = graphics.Turtle() # graphics board turtle pieces
        self.gbth = graphics.Turtle() # graphics board turtle highlight
        self.board = board
        self.parent = parent
        self.gbs.onclick(self.select_piece)
        self.gbs.onclick(self.h_clear, btn=3)

    def close(self):
        self.parent.b_open = False
        self.gbs.bye()
        self.parent.focus_force()

    def draw_board(self):
        self.gbts.clear()
        for col in self.board:
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
        for col in self.board:
            for row in col:
                if row.piece != None:
                    self.gbtp.goto((Vector(-4*scale, -4*scale)+row.pos*scale)+Vector(scale/2, -int(scale*0.15))) # moves to bottom center of square
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
        for sp in piece.check_moves():
            colour = (pallet[not sp.colour] if sp.piece == None else "red")
            self.draw_highlight(sp, colour, 2)

    def select_piece(self, x, y):
        click = Vector(x, y)
        click -= click % scale
        pos = Vector(*(int(a) for a in (click-Vector(-4*scale, -4*scale))/scale))
        if (-1 < pos[0] < 8) and (-1 < pos[1] < 8): # makes sure selection is on the board
            pos = self.board[pos[0]][pos[1]]
            val = self.board.select(pos)
            self.gbth.clear()
            if val == 1:
                self.draw_pieces()
            elif val == 2:
                self.draw_moves(pos.piece)
                self.draw_highlight(pos, "green", 2)
            elif val == 3:
                self.draw_moves(pos.piece)
                self.draw_highlight(pos, "red", 2)

    def h_clear(self, *args):
        self.board.highlight = None
        self.gbth.clear()

#---Pages----------------------------------------------------------------------#

class PageMenu(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Label(self, text="Welcome to Chess"), row=0, column=0, columnspan=3, pady=15, sticky="ew")
        self.add(gui.tk.Button(self, text="Game", command=lambda: self.show_page("game")), pady=5)
        self.add(gui.tk.Button(self, text="Network", command=lambda: self.show_page("network")), pady=5)
        self.add(gui.tk.Button(self, text="Options"), pady=5)

class PageGame(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Button(self, text="Menu", command=lambda: self.show_page("menu")), row=0, column=0, columnspan=3, pady=15, sticky="ew")
        self.add(gui.tk.Button(self, text="Board", command=self.play))
        self.add(gui.tk.Button(self, text="Save", command=self.save))
        self.add(gui.tk.Button(self, text="Load", command=self.load))
        self.add(gui.tk.Button(self, text="Leave", command=lambda: self.parent["network"].disconnect()))

    def play(self):
        if not self.parent.b_open:
            self.parent.b = Board(self.parent, self.parent.lb)
        self.parent.b.gbs.listen()
        self.parent.b.draw_board()
        self.parent.b.draw_pieces()

    def save(self, answer=False):
        answer = answer if answer else gui.tk.simpledialog.askstring("Save As", "Enter Save Name:", parent=self)
        iofile.write.pickle("saves/"+(answer if answer not in (None, "") else "save"), self.parent.lb, ext="sav")

    def load(self):
        answer = gui.tk.simpledialog.askstring("Load", "Enter Save Name:", parent=self)
        self.parent.lb = iofile.read.pickle("saves/"+(answer if answer not in (None, "") else "save"), ext="sav")

class PageNetwork(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Button(self, text="Menu", command=lambda: self.show_page("menu")), row=0, column=0, columnspan=3, pady=15, sticky="ew")
        if iofile.read.cfg("options")["network"]["allowed"]:
            self.add(gui.tk.Button(self, text="Chat", command=lambda: self.show_page("chat")))
            self.add(gui.tk.Button(self, text="Save", command=self.save))
            self.add(gui.tk.Button(self, text="Load", command=self.load))
            self.add(gui.tk.Button(self, text="Join", command=self.connect))
            self.add(gui.tk.Button(self, text="Leave", command=self.disconnect))
        else:
            self.add(gui.tk.Label(self, text="Networking is Disabled"))

    def save(self, answer=False):
        answer = answer if answer else gui.tk.simpledialog.askstring("Save File", "Enter Save Name:", parent=self)
        if answer in ("", None):
            file_name = "save"
        data = self.parent.nc.save(file_name, iofile.read.bin("saves/"+file_name, ext="sav"))
        if data:
            pass

    def load(self, answer=False):
        answer = answer if answer else gui.tk.simpledialog.askstring("Load File", "Enter Save Name:", parent=self)
        if answer in ("", None):
            answer = "save"
        data = self.parent.nc.load(answer)
        if data:
            self.parent.lb = data

    def connect(self):
        answer = gui.tk.simpledialog.askstring("IP", "Enter IP Address:", parent=self)
        if answer in ("", None):
            ip = iofile.read.cfg("options")["network"]["address"]
        elif len(answer.split(".")) == 4 and all([(i.isdigit()) and (0 < len(i) < 4) for i in answer.split(".")]):
            ip = answer
        else:
            return False
        self.parent.

    def disconnect(self):
        pass

class PageChat(gui.Page):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.add(gui.tk.Button(self, text="Back", command=lambda: self.show_page("network")), row=0, column=0, columnspan=3, pady=15, sticky="ew")
        self.add(gui.tk.Label(self, text="HELLO"))

#---Functions------------------------------------------------------------------#
