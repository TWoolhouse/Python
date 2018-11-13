import vote
from random import randint

options = ["America", "Club", "Fairy", "Moon?", "80's"]
sims = 10000
output = False

def make_pop():
    blts = []
    for p in range(240):
        vs = []
        for v in range(randint(2, 5)):
            v = randint(0, 5)
            if not v:
                break
            vs.append(options[v-1])
        blts.append(vote.Ballot(*vs))
    return blts

vote.size(5)
vote.pop(1)

wins = {k : 0 for k in options}

for i in range(1, sims+1):
    x = vote.vote(*make_pop(), output=output)
    if not i % 10:
        print(i)
    for j in x:
        wins[j] += 1

print("\n"+", ".join("{}: {}%".format(k, int(wins[k]/sims*100)) for k in wins))
