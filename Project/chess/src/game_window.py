from src.log import log
from src.states import State
from src.properties import Properties

import libs
import graphics
import util

class Window:
    def __init__(self, name):
        GameProperties.name = name
        self.screen = None

        State(State.TurtleWindow, State.TurtleWindow.Closed)

    def open(self):
        if State(State.TurtleWindow.Closed):
            self.screen = Screen()
            graphics.turtle.listen()
        elif State(State.TurtleWindow.Open):
            graphics.turtle.listen()
        else:
            log.warning("Trying to open Screen with invalid State.TurtleWindow %s", State(State.TurtleWindow))

    def update(self):
        if State(State.TurtleWindow.Open):
            self.screen.update()

class GameProperties:
    name = "GAME"
    width = 800
    height = 800

class Turtle:
    buffer = True
    def __init__(self):
        self.turtle_a = graphics.Turtle()
        self.turtle_b = graphics.Turtle()
    def __call__(self):
        return self.turtle_a if Turtle.buffer else self.turtle_b
    def update(self):
        Turtle.buffer = not Turtle.buffer
        return self

class Screen:
    def __init__(self):
        self.screen = graphics.Screen(GameProperties.name, (GameProperties.width, GameProperties.height))
        self.screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", self.close)
        graphics.turtle.TurtleScreen._RUNNING = True # Allows the screen to be opened again, because Turtle is really well made
        self.t_board, self.t_piece, self.t_highlight = Turtle(), Turtle(), Turtle()
        self.event_buffer = list()

        self.screen.onclick(self.event_click, btn=1)
        self.screen.onclick(self.event_clear, btn=3)

        self.update()

        State(State.TurtleWindow, State.TurtleWindow.Open)

    def event(func):
        def event(self, *args, **kwargs):
            self.event_buffer.append((func, args, kwargs))
        return event

    def update(self):
        for func, args, kwargs in self.event_buffer:
            func(self, *args, **kwargs)
        self.event_buffer.clear()
        self.screen.update()

    def close(self):
        State(State.TurtleWindow, State.TurtleWindow.Closed)
        self.screen.bye()

    def draw(self):
        for square in Properties.board().grid.all():
            util.contrain(square.pos)

    @event
    def event_click(self, x, y):
        log.debug("%d: CLICK (%d, %d)", Properties.delta_time().frame_count, x, y)
    @event
    def event_clear(self, *args):
        log.debug("%d: CLEAR", Properties.delta_time().frame_count)
