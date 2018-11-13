from fraction import Fraction

class Variable:

    def __init__(self, letter, quantity=1, value=None):
        self.letter, self.value, self.quantity = letter, value, quantity

    def __str__(self):
        if type(self.quantity) == Fraction:
            return "{}{}/{}".format(self.quantity.numerator, self.letter, self.quantity.denominator)
        return "{}{}".format(self.quantity if self.quantity != 1 else "", self.letter)

# x = Variable("a", Fraction(3, 5))
# print(x)
x = Fraction(2, 5)
x *= 4
print(type(x), x)
