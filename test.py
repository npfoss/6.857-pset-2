from random import randint

n = 100000
s = 0
for i in range(n):
    r = randint(0, 1408)
    s += r / 4.0 - int(r/4)

print s / n


# answer: 3/8, as expected