class Fraction:

    def __init__(self, numerator, denominator=1.0):
        # if type(numerator) == type(self):
        #     denominator = numerator.denominator
        #     numerator = numerator.numerator
        expn = 0
        while not (float(numerator*10**expn).is_integer() and float(denominator*10**expn).is_integer()):
            expn += 1
        self.numerator, self.denominator = int(numerator*10**expn), int(denominator*10**expn)
        self.simplify()

    def simplify(self):
        prev = None
        while prev != self.numerator:
            prev = self.numerator
            for i in range(2, ((self.numerator if self.numerator < self.denominator else self.denominator) if (self.numerator if self.numerator < self.denominator else self.denominator) < 1000000 else 1000000)+1):
                if (not self.numerator % i) and (not self.denominator % i):
                    self.numerator, self.denominator = int(self.numerator / i), int(self.denominator / i)
                    break

    def __str__(self):
        return "{}/{}".format(self.numerator, self.denominator)
    def __int__(self):
        return self.numerator//self.denominator
    def __float__(self):
        return self.numerator/self.denominator

    def __add__(self, other):
        if type(other) == type(self):
            return self.__class__((self.numerator*other.denominator)+(other.numerator*self.denominator), self.denominator*other.denominator)
        return self+Fraction(other)

    def __sub__(self, other):
        if type(other) == type(self):
            return self.__class__(self.numerator*other.denominator-other.numerator*self.denominator, self.denominator*other.denominator)
        return self-Fraction(other)

    def __mul__(self, other):
        if type(other) == type(self):
            return self.__class__(self.numerator*other.numerator, self.denominator*other.denominator)
        return self*Fraction(other)

    def __truediv__(self, other):
        if type(other) == type(self):
            return self.__class__(self.numerator*other.denominator, self.denominator*other.numerator)
        return self/Fraction(other)

    def __pow__(self, other):
        pass

x = Fraction(-4, -6)
print(x)
