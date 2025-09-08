# ***************************************************************************
# $Id $
# **************************************************************************/
##
# @file     tsm/anneal.py
# @brief    simulated annealing solution of the traveling salesman problem (TSM)
# @author   Markus Quandt  \n<markus.quandt@uni-tuebingen.de>
# 
# $Date: 2021/06/28 00:43:44 $
# $Revision: cd9b473d1654 $
#
# *************************************************************************/

import argparse
import os.path
import random
import sys
import json
import math
import numpy as np
import time
import itertools
import tsm_plot


# --------------------------------------------------------------------------
# main computation routines
# --------------------------------------------------------------------------

# Target function: total length of a permutation of cities, according to the 
# distance matrix passed as second arguments.
# perm     : random permutation of 0,...,N-1
# distance : the distance matrix
# NOTE: The tour is closed, i.e. the length includes the last segment
# from perm[N-1] back to perm[0]
def target(perm, distance) :
    N = len(perm)
    dist  = distance[perm[N-1], perm[0]]   # last segment to close tour
    for i in range(N-1):
        dist += distance[perm[i], perm[i+1]]
    return dist                     
     

# make a few random updates and record the changes dE in the target 
# functional. Inititalize T >> dE and perm to random permutation,
# then return (perm, T)
def init(distance, num, fac) :
    N, _ = distance.shape
    cities = np.arange(N)
    p = np.random.permutation(cities)
    E = target(p, distance)
    dE = 0 
    for i in range(num) : 
        p = np.random.permutation(cities)
        V = target(p, distance)
        d = abs(V - E)
        E = V;
        if d > dE :
            dE = d
    T = fac * dE
    return p, T
    

# reverse the section [a, a+l-1] of perm
# a : in the range 0,...,N-1
# l : in the range 0,...,N-1
# These conditions are not checked for efficiency.
# If b := a + l  > N, set k = a + l - N and 
# cycle left by k steps; also set a = a-k and b = b-k = N.
# Then reverse the index range [a,b[ (excluding the end-index b)
# and return the modified permutation
def reverse(perm, a, l):
    N = len(perm)
    b = a + l
    if b > N : 
        k = a + l - N
        a -= k
        b -= k
        perm1 = np.roll(perm, -k)  # makes a copy
    else :
        perm1 = np.copy(perm)      # makes a copy
    perm1[a:b] = perm1[a:b][::-1]
    return perm1


# cut out the section [a, a+l-1] of perm and insert it 
# a : in the range 0,...,N-1
# l : in the range 0,...,N-1
# These conditions are not checked for efficiency.
# If b := a + l  > N, set k = a + l - N and 
# cycle left by k steps; also set a = a-k and b = b-k = N.
# Then cut the sub-array [a,b] (excluding the end-index), 
# and reinsert the cut-out piece at any location, which may
# not  be the original location (c != a)
def relocate(perm, a, l):
    N = len(perm)
    b = a + l
    if b > N : 
        k = a + l - N
        a -= k
        b -= k
        perm1 = np.roll(perm, -k)     # makes a copy
    else :
        perm1 = np.copy(perm)         # makes a copy
    sec = perm1[a:b]
    perm1 = np.delete(perm1,np.s_[a:b])
    while True:
        c = random.randint(0, len(perm1))
        if c != a :
            break
    return np.insert(perm1, c, sec) 


# a potential update of the best permutation: either a reverse() or a 
# relocate() with random starting point and length
# NOTE: This returns a modified copy of perm; it does not modify perm
def update(perm) : 
    N = len(perm)
    a = random.randint(0, N-1)
    l = random.randint(0, N-1)
    return reverse(perm, a, l) if random.getrandbits(1) else relocate(perm, a, l)


# This class stores information about the performance of the algorithm 
# at each temperature, and the final result
class history:
    def __init__(self):
        self.__T = []
        self.__suc = []
        self.__tot = []
        self.__perm = []
        self.__E = []
        
    def record(self, T, tot, suc, perm, E) :
        self.__T.append(T)
        self.__suc.append(suc)
        self.__tot.append(tot)
        self.__perm.append(perm)
        self.__E.append(E)
        
    def last_target(self, num = 0):
        if num < 1 : 
            num = len(self.__E)
        vals = self.__E[-num:]
        return max(vals), min(vals)
    
    def all_targets(self):
        return self.__E
    
    def last(self):
        try : 
            return self.__T[-1], self.__tot[-1], self.__suc[-1], self.__perm[-1], self.__E[-1]
        except:
            return ()
        
    def size(self) : 
        return len(self.__T)
    
    def total(self):
        return sum(self.__tot)
    
    def temp_range(self):
        try:
            return max(self.__T), min(self.__T)
        except:
            return ()
        
    def best(self):
        try:
            return self.__perm[-1], self.__E[-1]
        except:
            return ()
                

# the main computation method
def compute(distance): 
    # get problem size N
    rows,cols = distance.shape
    if rows != cols or rows < 2: 
        raise ValueError;
    N = rows
     
    # some hard-coded constants
    inum = 10*N            # number of random searches in init() to determine dE 
    ifac = 5.0              # initial T is factor ifac the typical dE
    eps  = 0.0001           # minimal fractional change to trigger convergence
    cnum = 3                # number of temperatures with no change to trigger convergence
    fac  = 0.90             # temperature reduction factor
    xsuc = 10*N             # move to next T after this number of E reductions
    xtot = 100*N            # move to next T after tis number of total update attempts
    
    # initialize
    perm, T = init(distance, inum, ifac)
    E = target(perm, distance)
    converged = False
    
    # bookkeeping: history collects statistical information for each temperature
    histo = history()
    
    # main loop
    suc = 0
    tot = 0
    while True : 
        # Metropolis
        perm1 = update(perm)
        E1 = target(perm1, distance)
        tot += 1 
        if E1 < E : 
            perm = perm1
            E = E1
            suc += 1
        else :
            dE = E1 - E
            r = math.exp(- dE / T)
            q = random.random()
            if(q < r) : 
                perm = perm1
                E = E1
        # check if we're done at this temperature
        if tot > xtot or suc > xsuc : 
            # okay: store results at this temperature
            Ex = target(perm, distance)
            histo.record(T, tot, suc, perm, E)
           
            # check convergence: no substantial reduction at last temperatures
            # make at least ten reduction steps to avoid spurious convergence
            if histo.size() > max(cnum, 10) :
                Emax, Emin = histo.last_target(cnum)
                if (Emax - Emin) < eps * Emax : 
                    converged = True
                    break;
                
            # not converged: reduce temperature
            suc = 0
            tot = 0
            T *= fac;
             
    # we have converged
    return histo
    
    
# --------------------------------------------------------------------------
# the main entry point
# --------------------------------------------------------------------------

def main():
    # parse command line arguments
    print("")
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input file with TSM problem as json")
    args = parser.parse_args()
    prog = os.path.basename(__file__)
    infile = args.infile
    print(f"   + reading input file '{infile}'")
    
    # read problem from input file
    cities = []
    try:
        with open(infile, "r") as f : 
            cities = json.load(f)
            count  = len(cities)
    except:
        print(f"{prog}: error: input file corrupted or invalid json data")
    print(f"   + found TSM problem with N={count} cities") 
            
    # create distance matrix
    print(f"   + setting up distance matrix")
    distance = np.zeros([count,count])
    irange = range(count)
    for i in irange :
        for k in irange :
            a = cities[i]
            b = cities[k]
            d0 = a[0]-b[0]
            d1 = a[1]-b[1]
            distance[i, k] = math.sqrt(d0*d0 + d1*d1)
            
    # do computation, take timings
    print(f"   + starting calculation, this may take some time ... ")
    try:
        start = time.perf_counter()
        histo = compute(distance)  
        stop  = time.perf_counter()
    except:
        print(f"{prog}: error: internal error in main computation")
        sys.exit()
    print(f"   + finished calculation")
    
    # get solution and timings
    Tmax, Tmin = histo.temp_range()   
    nsteps = histo.size()
    total = histo.total()
    sol, Emin = histo.best()
    
    # prepare solution for display:
    #   - cycle such that city #0 is in slot 0
    #   - add city #0 as last city to complete tour
    #   - reverse solution if sol[1] > sol[-2] 
    # The last convention ensures that the tour is always run in 
    # the same direction, which simplifies the comparision of 
    # different solutions
    xsol = np.roll(sol, -np.where(sol==0)[0]).tolist()
    xsol.append(0)
    if len(xsol) > 2 and  xsol[1] > xsol[-2] :
        xsol.reverse()
    
    # present results
    print("\n-----------\n")
    print(f"   + size          : {count}")
    print(f"   + Tmax          : {Tmax}")
    print(f"   + Tmin          : {Tmin}")
    print(f"   + T steps       : {nsteps}")
    print(f"   + total updates : {total}")
    if len(xsol) > 14 : 
        print(f"   + solution      : [", end='')
        for i in range(14) : 
            print(f"{xsol[i]}, ", end='')
        print(f"{xsol[14]} ... ]")
    else:
        print(f"   + solution      : {xsol}")
    print(f"   + length        : {Emin}")
    print(f"   + CPU time      : {stop - start} seconds")
  
    # plot solution
    print("")
    tsm_plot.plot(cities,xsol)
    return 


# --------------------------------------------------------------------------
# run main() as a script only, not when importing this file as a module
# --------------------------------------------------------------------------

if __name__ == "__main__":
    main()
