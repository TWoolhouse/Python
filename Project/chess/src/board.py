from src.log import log
from src.states import State
from src.properties import Properties

import enum

import libs
from vector import Vector

board = None

SIZE = 8

@enum.unique
class Colour(enum.IntEnum):
    Black = 0
    White = 1

class Grid:
    def __init__(self, value):
        self.grid = [[value(x, y) for x in range(SIZE)] for y in range(SIZE)]
    def __getitem__(self, pos, pos2=None):
        if pos2 == None:
            return self.grid[pos[0]][pos[1]]
        return self.grid[pos][pos2]
    def __setitem__(self, pos, pos2, piece=None):
        if piece == None:
            self.grid[pos[0]][pos[1]].piece = pos2
        else:
            self.grid[pos][pos2].piece = piece
    def __iter__(self):
        return self.grid.__iter__()
    def all(self):
        for y in self.grid:
            for x in y:
                yield x

class Board:
    def __init__(self):
        self.grid = Grid(Square)
        self.player = Colour.White
        self.state = State.Board.Null
        self.activate()

    def activate(self):
        global board
        board.state = State.Board.Closed
        State(State.Board, State.Board.Closed)
        board = self
        self.state = State.Board.Active
        State(State.Board, State.Board.Active)

    def update(self):
        pass

    def clear(self):
        for space in self.grid.all():
            space.piece = None

    def build(self):
        for c in range(2):
            row, off = (0, 1) if c else (SIZE-1, -1)
            for col in range(SIZE):
                PiecePawn(self.grid[col, row+off], Colour(c))
            for col, peice in enumerate((PieceRook, PieceKnight, PieceBishop, PieceQueen, PieceKing, PieceBishop, PieceKnight, PieceRook)):
                peice(self.grid[col, row], Colour(c))

    def select(self):
        pass

class Square:
    def __init__(self, x, y):
        self.pos = Vector(x, y)
        self.colour = Colour((y+(x % 2)) % 2)
        self.piece = None

    def move(self, piece=None):
        self.piece = piece

class Piece:
    def __init__(self, square, colour):
        self.square = square
        self.colour = colour
        self.square.move(self)

    def move(self, square):
        self.square.move()
        square.move(self)

    def contain(self, vec):
        if (-1 < vec[0] < SIZE) and (-1 < vec[1] < SIZE):
            return True
        return False

    def _check_move(self, vec):
        if self.contain(vec):
            if board.grid[vec].piece == None:
                return board.grid[vec]
            elif board.grid[vec].piece.colour != self.colour:
                return board.grid[vec]
        return False

    def _gen_moves(self):
        yield self.square.pos

    def calc_moves(self):
        res = list()
        gen = self._gen_moves()
        for vec in gen:
            square = self._check_move(vec)
            if square != False:
                res.append(square)
            else:
                gen.send(True)
        return res

class PiecePawn(Piece):
    pass
class PieceKnight(Piece):
    pass
class PieceRook(Piece):
    def _gen_moves(self):
        for dir in (0, 1):
            for rev in (-1, 1):
                failed = False
                for i in range(1, SIZE):
                    res = self.square.pos+Vector(i*(not dir)*rev, i*dir*rev)
                    failed = (yield res)
                    if failed:
                        yield
                        break
class PieceBishop(Piece):
    pass
class PieceQueen(Piece):
    pass
class PieceKing(Piece):
    pass
