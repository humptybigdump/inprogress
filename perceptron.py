#! ./env/bin/python

from random import choice
from numpy import array, dot, random

def ustep(x) :
    return 0 if x < 0 else 1


# input (x0, x1, dummy) -> output f(x0,x1)
# the dummy input x2=1 is to simplify the implementation of the bias as w[2]
# this represents the OR function
training_data = [
    (array([0,0, 1]), 1),
    (array([0,1, 1]), 1),
    (array([1,0, 1]), 1),
    (array([1,1, 1]), 0),
]


w = random.rand(3)   # weights (w[0],w[1]) and bias (w[2])
eta = 0.3            # learning rate
n = 1000             # number of training instances
errs = []            # record errors during training here


# train the network
print(f"\nTraining with {n} samples ...")
for i in range(n) :
    x, expected = choice(training_data)
    phi = dot(w,x)
    delta = expected - ustep(phi)
    errs.append(delta)
    w += eta * delta * x                 # delta rule


# test the trained network
print(f"Testing the trained system ...\n")
for x,_ in training_data:
    phi = dot(x,w)
    res = ustep(phi)
    print(f"{x[:2]}: {phi:+.4f} -> {res}")
print()

