import libs
import iofile
import graphics
import util

#---Global Variables-----------------------------------------------------------#

FOLDER = "Output/"
SIZE = (1280, 720)
TURTLES = 1

gs = graphics.Screen("City", (SIZE[0]+20, SIZE[1]+20))
gts = [graphics.Turtle() for i in range(TURTLES)]
t_count = -1

#---Classes--------------------------------------------------------------------#

#---Functions------------------------------------------------------------------#

def draw_element(ty, value, x, y, mx, sx, my, sy):
    t = assign()
    x = util.constrain(x, 0, mx, -sx,  sx)
    y = util.constrain(y, 0, my,  sy, -sy)
    t.goto(x, y)
    s = value_lookup(ty, t, value)
    if s > 2:
        t.pd()
        t.dot(s)
        t.pu()

def main(grid, *tys):
    global colours
    # for t in gts:
    #     t.clear()
    updated_percent = set()
    time_taken = []
    sx, sy = SIZE[0] // 2, SIZE[1] // 2
    for pos, data in grid["data"]:
        for ty in tys:
            draw_element(ty, data.data[ty], *pos, grid["width"], sx, grid["height"], sy)
        percent = int(pos[0] / grid["width"] * 100)
        if percent not in updated_percent:
            updated_percent.add(percent)
            gs.update()
    gs.update()
    print("Drawing Complete!")

def loop():
    gs.mainloop()

#---Setup----------------------------------------------------------------------#

#---Main Loop------------------------------------------------------------------#

#---End------------------------------------------------------------------------#
