import src
from src.log import log
from src.states import State
from src import properties
from src import window
from src import board

import time

class DeltaTime:
    frame_count = 0
    def __init__(self, tick_rate):
        self.current = time.time()
        self.tick_rate = tick_rate
        self.__call__()
    def __call__(self):
        self.previous = self.current
        self.current = time.time()
        self.time = self.current - self.previous
        DeltaTime.frame_count += 1
        return self
    def sleep(self):
        sleep = (self.tick_rate-self.time) / 2
        time.sleep(sleep if sleep > 0 else 0)
        return self

class Game:
    def __init__(self, ups=60):
        State(State.Game, State.Game.Null)
        self.callback = dict()

        self.window = window.Window("Chess")
        self.board = board.Board()
        self.delta_time = DeltaTime(2/ups)

        #Assigning Property Callbacks
        properties.Properties.board = lambda: self.board
        properties.Properties.window = lambda: self.window
        properties.Properties.delta_time = lambda: self.delta_time

    def update(self):
        global dev_frame_count
        self.window.update()
        self.delta_time().sleep()

game = Game()
while not State(State.Game.Quit):
    game.update()
