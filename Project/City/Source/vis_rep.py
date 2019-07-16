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

class Node:
    pass

#---Functions------------------------------------------------------------------#

def assign():
    global t_count
    t_count = (t_count + 1) % TURTLES
    return gts[t_count]

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

# def value_lookup(t, value):
#     # print(value, type(value), type(value).__name__)
#     if type(value).__name__ == "Cell":
#         t.color("black")
#         return 1
#     elif type(value).__name__ == "Gap" and len(value.orientations) < 2:
#         t.color("blue")
#         return 1
#     elif type(value).__name__ == "Gap":
#         t.color("green")
#         return 1
#     elif type(value).__name__ == "Road":
#         t.color("red")
#         return 5
#     else:
#         t.color("white")
#         return 1

colours = ["yellow", "violet", "lightgreen", "chocolate", "gold", "navy", "gray", "cyan", "green", "skyblue", "darkgreen", "maroon", "magenta", "orange", "purple", "turquoise", "black", "blue"]
def value_lookup(ty, t, value):
    if ty == "road":
        if type(value).__name__ == "Road":
            t.color("red")
            return 6
        elif type(value).__name__ == "Gap" and len(value.orientations) < 2:
            t.color("blue")
            return 3
        elif type(value).__name__ == "Gap":
            t.color("green")
            return 3
    elif ty == "zone":
        if value:
            t.color(colours[value % len(colours)])
            return 1
    t.color("white")
    return 1

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

if __name__ == "__main__":
    grid = iofile.read.pickle(FOLDER+"output", ext="raw")
    main(grid)

#---End------------------------------------------------------------------------#

    gs.mainloop()
