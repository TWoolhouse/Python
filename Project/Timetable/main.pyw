import datetime
import winsound

import libs
import iofile
import gui

FILE_NAME = "school"

mon = datetime.date(2019, 3, 4)
week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
week_day = week[(datetime.datetime.today().date()-mon).days % 7]
meridiem = datetime.datetime.now().hour < 12
days = []

class Subject:

    def __init__(self, name, min, count):
        self.name, self.min, self.count = name, int(min), int(count)
        self.left = datetime.timedelta(seconds=self.min*60, microseconds=1)
        self.prev = datetime.datetime.now()

    def __repr__(self):
        return "{} - {} - {}".format(self.name, self.min, self.count)

    def update(self, now):
        self.left -= now-self.prev
        self.prev = now
        return self.left

    def update_time(self):
        self.prev = datetime.datetime.now()

class Day:
    def __init__(self, name, start, *subs):
        self.name = name
        self.start = datetime.time(*(int(i) for i in start.split(":")))
        self.meridiem = self.start.hour < 12
        self.subs = list(subs)
    def __repr__(self):
        return "\n".join((str(i) for i in self.subs))
    def __iter__(self):
        return self.subs.__iter__()
    def __len__(self):
        return self.subs.__len__()
    def __getitem__(self, key):
        return self.subs.__getitem__(key)

    def update_time(self):
        for i in self.subs:
            i.update_time()

class PageExit(gui.Page):

    open = True

    def setup(self):
        for func in ((self.exit, "<Return>"), (lambda *k: self.show_page("day"), "<BackSpace>"),
                    (self.minimize, "<Escape>"), (self.demin, "<FocusIn>")):
            for key in func[1:]:
                self.bind(key, func[0])
        self.add(gui.tk.Label(self, text="Are You Sure You Want to Quit?\n\n\n\nEnter"), row=0, column=0, columnspan=5, rowspan=5, pady=15, sticky="nsew")

    def show(self):
        self.focus_set()

    def demin(self, key):
        self.unbind("<FocusIn>")
        self.parent.state("zoomed")
        #self.parent.overrideredirect(1)
        self.show_page("day")

    def minimize(self, *key):
        self.bind("<FocusIn>", self.demin)
        self["_temp"].focus_set()
        self.parent.overrideredirect(0)
        self.parent.state("normal")
        self.parent.geometry("1x1")
        self.parent.state("iconic")
        self.focus_set()

    def exit(self, key):
        self.open = False

class PageDay(gui.Page):

    def setup(self, day):
        self.day = day
        self.button = gui.tk.IntVar()
        for func in ((self.pause, "<space>", "<Pause>", "<Return>"), (self.exit, "<Escape>"),
                    (lambda *k: self.show_page("table"), "<BackSpace>"),
                    (self.pause, "<FocusOut>")):
            for key in func[1:]:
                self.bind(key, func[0])
        self.add(gui.tk.Label(self, text=day.name+(" Morning" if day.meridiem else " Evening")), row=0, column=0, columnspan=5, pady=15, sticky="nsew")
        self.add(gui.tk.Label(self, text="Total"), "total", row=1, column=0, columnspan=5, pady=5, sticky="nsew")
        self.add(gui.tk.Label(self, text="Start: "+str(self.day.start)), row=2, column=0, columnspan=2, pady=5, sticky="nsew")
        self.add(gui.tk.Label(self, text="Pause:"), row=2, column=2, pady=5, sticky="nse")
        self.add(gui.tk.Radiobutton(self, variable=self.button, value=-1, command=self.show), row=2, column=3, pady=5, sticky="nsew")
        self.add(gui.tk.Label(self, text="Subject"), row=3, column=0, pady=15, padx=5, sticky="nsew")
        self.add(gui.tk.Label(self, text="Pages"), row=3, column=1, pady=15, padx=5, sticky="nsew")
        self.add(gui.tk.Label(self, text="Time"), row=3, column=2, pady=15, padx=5, sticky="nsew")
        self.button.set(-1)
        self.buttons = []
        for s in range(len(day)):
            self.buttons.append(gui.tk.IntVar())
            self.add(gui.tk.Label(self, text=day[s].name), row=4+s, column=0, padx=5, sticky="nsew")
            self.add(gui.tk.Label(self, text=day[s].count), row=4+s, column=1, padx=5, sticky="nsew")
            self.add(gui.tk.Label(self, text=str(day[s].left)[:-7]), s, row=4+s, column=2, padx=5, sticky="nsew")
            self.add(gui.tk.Radiobutton(self, variable=self.button, value=s, command=self.day.update_time), row=4+s, column=3, padx=5, sticky="nsew")
            self.add(gui.tk.Checkbutton(self, variable=self.buttons[s], command=self.day.update_time), row=4+s, column=4, padx=5, sticky="nsew")

    def show_page(self, *args):
        self.pause()
        super().show_page(*args)

    def show(self):
        self.focus_set()

    def pause(self, *key):
        self.button.set(-1)

    def exit(self, *key):
        if self.button.get() == -1:
            self.show_page("exit")
        else:
            self.pause()

    def update(self):
        now = datetime.datetime.now()
        self.edit("total", "text", str(now)[:-7])
        for s in range(len(self.day)):
            c = "black"
            if self.buttons[s].get():
                c = "green"
            if self.button.get() == s:
                if self.buttons[s].get():
                    self.button.set(-1)
                else:
                    t = self.day[s].update(now)
                    v = str(t)[:-7]
                    c = "blue"

                    if t.days < 0:
                        t = -t
                        v = "+"+str(t)[:-7]
                        c = "red"

                    self.edit(s, "text", v)
            self.edit(s, "fg", c)

class PageTable(gui.Page):

    meridiem = meridiem
    day = week_day

    def setup(self):
        for func in ((lambda *k: self.show_page("exit"), "<Escape>"),
                    (lambda *k: self.show_page("day"), "<BackSpace>"), (self.reload_day, "<Return>"),
                    (self.set_day, *range(1,8)), (self.set_meridiem, "w"), (self.reset, "r"),
                    (lambda *k: self.increment_day(1), "e"), (lambda *k: self.increment_day(-1), "q"),
                    (self.save, "s"), (self.load, "a"), (read_data, "l")):
            for key in func[1:]:
                self.bind(key, func[0])
        self.add(gui.tk.Label(self, text="Select a New Table"), row=0, column=0, columnspan=5, pady=15, sticky="nsew")
        self.add(gui.tk.Label(self, text=self.day), "info", row=1, column=0, columnspan=5, sticky="nsew")

    def update(self):
        self.edit("info", "text", self.day+(" Morning" if self.meridiem else " Evening"))

    def show(self):
        self.focus_set()
        self.day = self.parent["day"].day.name
        self.meridiem = self.parent["day"].day.meridiem

    def increment_day(self, amt):
        self.day = week[(week.index(self.day)+amt)%7]

    def set_day(self, key):
        self.day = week[int(key.keysym) - 1]

    def set_meridiem(self, key):
        self.meridiem = not self.meridiem

    def reload_day(self, key):
        PageDay(self.parent, "day", pick_day(days, self.day, self.meridiem))
        self.show_page("day")

    def reset(self, key):
        self.day = week_day
        self.meridiem = meridiem
        self.reload_day(key)

    def save(self, *key):
        iofile.write.pickle("_temp", self.parent["day"].day, ext="sav")

    def load(self, *key):
        PageDay(self.parent, "day", iofile.read.pickle("_temp", ext="sav"))
        self.show_page("day")

def read_data(file_name=FILE_NAME):
    global days
    data = iofile.read.cfg(file_name, ext="txt")
    days = [Day(k.split("-")[0], data[k]["start"], *[Subject(i, *data[k][i].split("-")) for i in data[k] if i != "start"]) for k in data]
    return days

def pick_day(days, week_day, meridiem):
    for d in days:
        if d.name == week_day and ((d.start.hour < 12) if meridiem else (d.start.hour > 12)):
            return d
    else:
        for d in days:
            if d.name == week_day:
                return d

days = read_data()

window = gui.Window("Timetable", 1280, 720, "Inconsolata 20")

window.state("zoomed")
#window.overrideredirect(1)

PageExit(window, "exit")
PageDay(window, "day", pick_day(days, week_day, meridiem))
PageTable(window, "table")
window.show_page("day")

while window["exit"].open:
    window.update()
