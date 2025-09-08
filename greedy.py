# ***************************************************************************
# $Id $
# **************************************************************************/
##
# @file     tsm/greedy.py
# @brief    Greedy solution of the traveling salesman problem (TSM)
# @author   Markus Quandt  \n<markus.quandt@uni-tuebingen.de>
# 
# $Date: 2021/06/28 00:43:44 $
# $Revision: cd9b473d1654 $
#
# *************************************************************************/

import argparse
import os.path
import sys
import json
import math
import numpy
import time
import itertools
import tsm_plot


# --------------------------------------------------------------------------
# main computation routines
# --------------------------------------------------------------------------

# measure the total length of a permutation of cities, according to the 
# distance matrix passed as second arguments.
# NOTE: The tour must be closed, and starts/ends at #0. The permutation
#       'perm' thus only contains the remaining city list, which is a 
#       permutation of 1,...,count=N-1 only !!
#
def measure(perm, distance) :
    count = len(perm)               # N-1
    # the two pieces involving the start/end city #0
    dist  = distance[0, perm[0]] 
    dist += distance[perm[-1], 0]
    # the pieces not involving #0, a total of count-1 = N-2
    for i in range(count-1):
        dist += distance[perm[i], perm[i+1]]
    # we have summed all (N-2)+2 = N pieces
    return dist                     
        

# Start at city #0 and travel successively to the nearest non-visited city.
# The result is a tour [0,....] starting at 0 but *not* including the final 0
# (this will be added in the main routine below). The returned distance will
# include the last piece back to 0.
def compute(distance):    
    count, cols = numpy.shape(distance)
    if cols != count :
        raise ValueError
    pool = set(range(1, count))
    sol  = [0]
    num  = 1
    cur  = 0
    dist = 0
    while num < count : 
        # search next city greedily
        dmin = 10   # impossible value
        for city in pool :
            d = distance[cur, city]
            if d < dmin :
                dmin = d
                next = city
        # update solution
        num += 1
        dist += dmin
        sol.append(next)
        cur = next
        pool.remove(next)
    # add last segment back to 0 to the total distance
    dist += distance[sol[-1], 0]
    # return solution
    return sol, dist
    
    
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
    distance = numpy.zeros((count,count))
    for i in range(count) :
        for k in range(count) :
            a = cities[i]
            b = cities[k]
            d0 = a[0]-b[0]
            d1 = a[1]-b[1]
            distance[i, k] = math.sqrt(d0*d0 + d1*d1)
            
    # do computation, take timings
    print(f"   + starting calculation, this may take some time ... ")
    try:
        start = time.perf_counter()
        sol, res = compute(distance)  
        stop = time.perf_counter()
    except:
        print(f"{prog}: error: internal error in main computation")
        sys.exit()
    print(f"   + finished calculation")
    
    # prepare solution for display:
    #   - cycle such that city #0 is in slot 0  [automatically ensured by program]
    #   - add city #0 as last city to complete tour
    #   - reverse solution if sol[1] > sol[-2] 
    # The last convention ensures that the tour is always run in 
    # the same direction, which simplifies the comparision of 
    # different solutions
    sol.append(0)
    if len(sol) > 2 and sol[1] > sol[-2]:
            sol.reverse()
    
    # present solution and timings
    print("\n-----------\n")
    print(f"   + size     : {count}")
    print(f"   + solution : {sol}")
    print(f"   + length   : {res}")
    print(f"   + CPU time : {stop - start} seconds")
    
    # plot solution
    print("")
    tsm_plot.plot(cities,sol)
    return 


# --------------------------------------------------------------------------
# run main() as a script only, not when importing this file as a module
# --------------------------------------------------------------------------

if __name__ == "__main__":
    main()
