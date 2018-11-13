import libs

# yyyy mm tmax tmin rain sun

class Month:

    def __init__(self, year, month, tmax, tmin, af, rain, sun, *extra):
        self.year, self.month, self.tmax, self.tmin, self.af, self.rain, self.sun, self.extra = int(year), int(month), float(tmax), float(tmin), int(af), float(rain), float(sun), extra
        self.provisional = True if "Provisional" in self.extra else False

    def __repr__(self):
        return "{} {} {} {} {} {} {} {}".format(\
        self.year, self.month, self.tmax, self.tmin, self.af, self.rain, self.sun, ", ".join(self.extra))

with open("data.txt", "r") as file:
    data = [Month(*line.replace("*","").split()) for line in file.readlines()]

highest = Month(0, 0, -271, -273, -1, -1, -1)
for temp in data:
    print(temp.tmax)
    if temp.tmax > highest.tmax:
        if not temp.provisional:
            highest = temp

print(highest)
