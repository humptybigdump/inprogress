#!/usr/bin/env python 

# simple implementation of a linear congruential generators (LCG)
# T. Ferber, April 2022, 
# further simplified and translated by U. Husemann, April 2024

# x_i =(a * x_i-1 + c) mod m
# return value: r_i =x_i/m, with r_i in [0,1[
# Important: good initial values (m: prime number, c = 0)
def lcg( seed, m = 2**31-1, a = 1140671485, c = 0 ):
    next  = (a*seed + c) % m
    return next/m, next

# number of random numbers to be generated
n = 10

# seed: from now on the sequence is deterministic
seed = 1

for i in range( n ):
    rnd, seed = lcg(seed)
    print(i, rnd)