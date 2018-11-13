import libs
from vector import Vector

class Board:

    def __init__(self):
        self.grid = [[Square((i+(j % 2)) % 2, Vector(i, j)) for j in range(8)] for i in range(8)]
        self.out = [[], []]
        self.player = 1
        self.highlight = None

    def __iter__(self):
        return self.grid.__iter__()
    def __getitem__(self, key):
        return self.grid[key]
    def __setitem__(self, key, value):
        self.grid[key] = value

    def clear(self):
        for col in self:
            for row in col:
                row.piece = None
        self.out = [[], []]
    def build(self):
        for j in range(2): # adds all the pieces to the board
            row, po = (0, 1) if j else (7, -1)
            for i in range(8): # Pawns
                Pawn(j, self[i][row+po], self)
            for k, v in enumerate((Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)):
                v(j, self[k][row], self)

    def select(self, selection):
        val = 0
        if (self.highlight != None) and (self.highlight.piece != None) and (selection in self.highlight.piece.check_moves()) and (self.highlight.piece.colour == self.player):
            self.highlight.piece.move(selection)
            val = 1
        elif (selection.piece != None):
            if (selection.piece.colour == self.player):
                val = 2
            else:
                val = 3
        self.highlight = selection
        return val

class Square:

    def __init__(self, colour, pos, piece=None):
        self.colour, self.pos, self.piece = colour, pos, piece

    def __repr__(self):
        return "{} : {} {}".format(self.piece, self.colour, self.pos)

class Piece:

    def __init__(self, colour, pos, board):
        self.colour, self.pos, pos.piece, self.board = colour, pos, self, board

    def __repr__(self):
        return "{} {}".format(self.colour, type(self).__name__)

    def move(self, space):
        self.pos.piece = None
        if space.piece != None:
            self.board.out[self.colour].append(space.piece)
        space.piece = self
        self.pos = space
        self.board.player = not self.board.player

    def constrain(self, space):
        if (-1 < space[0] < 8) and (-1 < space[1] < 8):
            return True
        return False

    def check_moves(self, *spaces):
        legit = []
        for set in spaces:
            for sp in set:
                if self.constrain(sp):
                    if self.board[sp[0]][sp[1]].piece == None:
                        legit.append(self.board[sp[0]][sp[1]])
                    elif (self.board[sp[0]][sp[1]].piece.colour != self.colour):
                        legit.append(self.board[sp[0]][sp[1]])
                        break
                    else:
                        break
                else:
                    break
        return legit

class Pawn(Piece): # en passant

    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.dir, self.turns = Vector(0, (1 if colour else -1)), 0

    def check_moves(self):
        return [*[self.board[sp[0]][sp[1]] for sp in [self.pos.pos+self.dir*i for i in range(1, (2 if self.turns else 3))] if (self.constrain(sp)) and (self.board[sp[0]][sp[1]].piece == None)], *[self.board[sp[0]][sp[1]] for sp in [self.pos.pos+self.dir+Vector(1*i, 0) for i in (-1, 1)] if (self.constrain(sp)) and (self.board[sp[0]][sp[1]].piece != None) and (self.board[sp[0]][sp[1]].piece.colour != self.colour)]]

    def move(self, space): # en passant
        self.turns += 1
        super().move(space)
class Knight(Piece):

    def check_moves(self):
        return super().check_moves(*[[self.pos.pos+Vector([1, 2][i]*dir*rev, [1, 2][(i-1)**2]*dir)] for i in (0, 1) for dir in (-1, 1) for rev in (-1, 1)])
class Bishop(Piece):

    def check_moves(self):
        return super().check_moves(*[[self.pos.pos+Vector(i*dir*-1, i*dir*rev) for i in range(1, 8)] for dir in (-1, 1) for rev in (-1, 1)])
class Rook(Piece):

    def check_moves(self):
        return super().check_moves(*[[self.pos.pos+Vector(i*(not dir)*rev, i*dir*rev) for i in range(1, 8)] for dir in (0, 1) for rev in (-1, 1)])
class Queen(Piece):

    def check_moves(self):
        return super().check_moves(*[*[[self.pos.pos+Vector(i*(not dir)*rev, i*dir*rev) for i in range(1, 8)] for dir in (0, 1) for rev in (-1, 1)], *[[self.pos.pos+Vector(i*dir*-1, i*dir*rev) for i in range(1, 8)] for dir in (-1, 1) for rev in (-1, 1)]])
class King(Piece): # castling

    def check_moves(self):
        return super().check_moves(*[[self.pos.pos+Vector((not dir)*rev, dir*rev)] for dir in (0, 1) for rev in (-1, 1)], *[[self.pos.pos+Vector(dir*-1, dir*rev)] for dir in (-1, 1) for rev in (-1, 1)])
