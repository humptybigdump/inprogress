# ***************************************************************************
# $Id $
# **************************************************************************/
##
# @file     tsm/ant.py
# @brief    Naive solution of the traveling salesman problem (TSM)
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
# Global parameters for the algorithm
# --------------------------------------------------------------------------

g_ant_count   = 10            # total number of ants

g_generations = 100           # maximal number of generations
g_check       = 3             # number of generations in convergence check
g_accuracy    = 0.00001       # accuracy goal in convergence test

g_intensity   = 10.0          # pheromone intensity factor Q
g_evap        = 0.5           # pheromone evaporation factor rho
g_alpha       = 1.0           # pheromone trail importance alpha
g_beta        = 10.0          # heuristics (visibility) importance beta
g_init        = 0.1           # initial pheromone level at all edges 


# --------------------------------------------------------------------------
# The ant agent 
# --------------------------------------------------------------------------

class ant :
    def __init__(self, distance, pheromone):
        # check arguments
        rows, cols = distance.shape
        if (rows != cols) or (rows < 1) : 
            raise ValueError("ant: invalid distance matrix in constructor")
        prows, pcols = pheromone.shape
        if (prows != rows) or (pcols != cols) :
            raise ValueError("ant: invalid pheromone matrix in constructor")
        # initialize class
        self.__dist   = distance
        self.__phero  = pheromone
        self.__count  = rows
        self.reset()
        
    def reset(self):
        self.__path = []
        self.__rest  = list(range(self.__count))
        n = random.randint(0, self.__count-1)
        self.extend(n)
        
    # check if the current path is complete
    def is_complete(self) : 
        return len(self.__path) == self.__count
    
    # check if the current path has an edge from i to k
    def has_edge(self, i, k):
        try:
            a = self.__path.index(i)
            b = self.__path.index(k)
            return abs(a-b) == 1
        except:
            return False
        
    # length of the current path in Euclidean metric
    def length(self):
        N = len(self.__path)
        s = 0
        if N > 1 :
            for i in range(N-1):
                s += self.__dist[self.__path[i], self.__path[i+1]]
            s += self.__dist[self.__path[-1], self.__path[0]]    # close path
        return s
    
    # extend the current path by adding a segment from the currently 
    # last city to the new city #n. This checks that n is from the 
    # list of non-visited cities, and the routine updates the current
    # tour length in self.__length
    def extend(self, n) :
        if n in self.__rest :
            self.__rest.remove(n)
            self.__path.append(n)
        else:
            # we have already visited n 
            raise ValueError("ant: cannot extend(), city already visited [internal]")
    
    # find a complete tour
    def solve(self):
        while not self.is_complete() :
            x = self.__path[-1]
            # find best next node based on visibility and pheromone
            q = []
            s = 0
            for y in self.__rest : 
                vis = 1/self.__dist[x,y]
                phe = self.__phero[x,y]
                r = (phe**g_alpha) * (vis**g_beta)
                s += r
                q.append(s)
            p = [r/s for r in q]        # p[-1] should be 1.0
            r = random.random()
            i = 0
            while r > p[i] :
                i += 1
            node = self.__rest[i]
            self.extend(node)           # will shrink __rest and grow __tour
        total = self.length()           # length of completed tour
        return self.__path, total
        

# --------------------------------------------------------------------------
# main computation routines
# --------------------------------------------------------------------------

def compute(distance): 
    # get problem size N
    rows,cols = distance.shape
    if rows != cols or rows < 2: 
        raise ValueError;
    N = rows
    irange = range(N)    
    
    # initialize pheromone matrix
    pheromone = np.full([N,N], g_init) 
    print("   + pheromone initialized")

    # create ant colony
    colony = set()
    count  = 0
    while count < g_ant_count :
        A = ant(distance, pheromone)    # arguments passed by reference
        colony.add(A)                   # i.e. changes in pheromone will be 
        count += 1                      # noticed by A
    print("   + ant colony created")
    
    # main loop
    gen    = 0
    histo  = []
    sol    = []                          # global solution
    best   = 100 * N                     # impossible value, tour length must be < N*sqrt(2)  
    print("   + starting main loop")
    while gen < g_generations : 
        # let all ants complete a tour
        for A in colony : 
            A.reset()                    # place at arbitrary start point, do not change pheromone
            tour, L = A.solve()          # solve from arbitrary start point at given pheromone
            if L < best:
                best = L
                sol  = tour
        histo.append(best)
        
        # Pheromone update
        for i in irange : 
            for k in irange :
                if(k == i) :
                    continue
                pherosum = 0
                for A in colony : 
                    if A.has_edge(i,k):
                        pherosum += 1/A.length()
                pheromone[i,k] = pheromone[i,k] * (1 - g_evap) + g_intensity * pherosum
        
        # check for convergence
        gen += 1
        if gen > g_check : 
            vals = histo[-g_check:]
            Lmin = min(vals)
            Lmax = max(vals)
            if abs(Lmax - Lmin) < abs(g_accuracy * Lmax) : 
                break  # converged
                
    # return result
    return sol, best, gen
                
    
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
    #try:
    start = time.perf_counter()
    sol, Lmin, niter  = compute(distance)  
    stop  = time.perf_counter()
    #except:
        #print(f"{prog}: error: internal error in main computation")
        #sys.exit()
    print(f"   + finished calculation")
    
    # prepare solution for display:
    #   - cycle such that city #0 is in slot 0
    #   - add city #0 as last city to complete tour
    #   - reverse solution if sol[1] > sol[-2] 
    # The last convention ensures that the tour is always run in 
    # the same direction, which simplifies the comparision of 
    # different solutions
    nsol = np.array(sol)
    xsol = np.roll(nsol, -np.where(nsol==0)[0]).tolist()
    xsol.append(0)
    if len(xsol) > 2 and  xsol[1] > xsol[-2] :
        xsol.reverse()
    
    # print results
    print("\n-----------\n")
    print(f"   + size          : {count}")
    print(f"   + ants          : {g_ant_count}")
    print(f"   + iterations    : {niter}")
    if len(xsol) > 14 : 
        print(f"   + solution      : [", end='')
        for i in range(14) : 
            print(f"{xsol[i]}, ", end='')
        print(f"{xsol[14]} ... ]")
    else:
        print(f"   + solution      : {xsol}")
    print(f"   + length        : {Lmin}")
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
