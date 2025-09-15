import lcg, tests, testa
import random


lcg1 = lcg.LCG(123456789, 101427, 321, 2**16)
numbers = lcg1.genNumbers(10000)
testa.kolmogorov_smirnov(numbers[0:100], 0.05)
testa.runs_test(numbers, 0.05, 4)

lcg2 = lcg.LCG(123456789, 65539, 0, 2**31)
numbers = lcg2.genNumbers(10000)
testa.kolmogorov_smirnov(numbers[0:100], 0.01)
testa.runs_test(numbers, 0.05, 4)


random.seed(123456789)
randomlist = []
for i in range(0,100000):
    n = random.random()
    randomlist.append(n)
testa.kolmogorov_smirnov(randomlist[0:100], 0.05)
testa.runs_test(randomlist, 0.05, 4)













































'''
Python uses Mersenne Twister algorithm for RNG
'''
