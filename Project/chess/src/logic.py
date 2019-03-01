import libs
from vector import Vector
from grid import Grid

class Board:

    def __init__(self):
        self.grid = Grid(8, 8)
        for i in range(8):
            for j in range(8):
                self.grid[i][j] = Square((i+(j % 2)) % 2, Vector(i, j))
        self.out = [[], []]
        self.player = 1
        self.selected = None

    def __repr__(self):
        return "{}".format("\n".join((str(i) for i in self.grid[::-1])))

    def clear(self):
        for space in self.grid.all():
            space.piece = None
    def build(self):
        for j in range(2): # both players
            row, off = (0, 1) if j else (7, -1) # bottom or top of board
            for i in range(8): # all the pawns
                Pawn(j, self.grid[i][row+off], self) # pawn with colour and row + offset
            for k, v in enumerate((Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)): # all the special pieces
                v(j, self.grid[k][row], self) # adding it to the board

    def select(self, selection):
        selection = self.grid[selection]
        val = 0
        if (self.selected != None) and (self.selected.piece != None) and (selection in self.selected.piece.check_moves()) and (self.selected.piece.colour == self.player):
            self.selected.piece.move(selection)
            val = 1 # if is a player's piece and correct space: move the piece
        elif (selection.piece != None):
            if (selection.piece.colour == self.player):
                val = 2 # select player's piece
            else:
                val = 3 # select opponet's piece

        self.selected = selection
        return val

class Square:

    def __init__(self, colour, pos, piece=None):
        self.colour, self.pos, self.piece = colour, pos, piece

    def __repr__(self):
        return "[{} {}] {}".format(self.pos, self.colour, self.piece)

class Piece:

    def __init__(self, colour, square, board):
        self.colour, self.square, self.board = colour, square, board
        self.square.piece = self

    def __repr__(self):
        return "{} {}".format(self.colour, type(self).__name__)

    def move(self, space):
        self.square.piece = None
        if space.piece != None:
            self.board.out[self.colour].append(space.piece)
        space.piece = self
        self.square = space
        self.board.player = not self.board.player

    def constrain(self, space):
        if (-1 < space[0] < 8) and (-1 < space[1] < 8):
            return True
        return False

    def check_moves(self, *spaces):
        print(spaces)
        legit = []
        for set in spaces:
            for space in set:
                if self.constrain(space):
                    if self.board.grid[space].piece == None:
                        legit.append(self.board.grid[space])
                    elif self.board.grid[space].piece.colour != self.colour:
                        legit.append(self.board.grid[space])
                        break
                    else:
                        break
                else:
                    break
        # print("LEGIT:", legit)
        return legit

class Pawn(Piece): # en passant

    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.dir, self.turns = Vector(0, (1 if colour else -1)), 0

    def check_moves(self):
        return super().check_moves([self.square.pos+self.dir*i for i in range(1, 2 if self.turns else 3)], *[[self.square.pos+self.dir+Vector(side, 0)] for side in (-1, 1) if self.constrain(self.square.pos+self.dir+Vector(side, 0)) and self.board.grid[self.square.pos+self.dir+Vector(side, 0)].piece != None])

    def move(self, space): # en passant
        self.turns += 1
        super().move(space)

class Knight(Piece):

    def check_moves(self):
        return super().check_moves(*[[self.square.pos+Vector([1, 2][i]*dir*rev, [1, 2][(i-1)**2]*dir)] for i in (0, 1) for dir in (-1, 1) for rev in (-1, 1)])
class Bishop(Piece):

    def check_moves(self):
        return super().check_moves(*[[self.square.pos+Vector(i*dir*-1, i*dir*rev) for i in range(1, 8)] for dir in (-1, 1) for rev in (-1, 1)])
class Rook(Piece):

    def check_moves(self):
        return super().check_moves(*[[self.square.pos+Vector(i*(not dir)*rev, i*dir*rev) for i in range(1, 8)] for dir in (0, 1) for rev in (-1, 1)])
class Queen(Piece):

    def check_moves(self):
        return super().check_moves(*[*[[self.square.pos+Vector(i*(not dir)*rev, i*dir*rev) for i in range(1, 8)] for dir in (0, 1) for rev in (-1, 1)], *[[self.square.pos+Vector(i*dir*-1, i*dir*rev) for i in range(1, 8)] for dir in (-1, 1) for rev in (-1, 1)]])
class King(Piece): # castling, check(mate)

    def check_moves(self):
        return super().check_moves(*[[self.square.pos+Vector((not dir)*rev, dir*rev)] for dir in (0, 1) for rev in (-1, 1)], *[[self.square.pos+Vector(dir*-1, dir*rev)] for dir in (-1, 1) for rev in (-1, 1)])
