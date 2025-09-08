# ***************************************************************************
# $Id $
# **************************************************************************/
##
# @file     tsm/generate.py
# @brief    Generates instances of the traveling salesman problem (TSM)
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



# --------------------------------------------------------------------------
# the main entry point
# --------------------------------------------------------------------------

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("count", help="the number of cities in the TSM problem")
    parser.add_argument("outfile", help="file in which to store the TSM description")
    args = parser.parse_args()
    prog = os.path.basename(__file__)
    outfile = args.outfile
    count   = 0
    try:
        count = int(args.count)
        if(count <= 0) :
            raise ValueError
    except ValueError:
        print(f"{prog}: error: 'count' must be a positive integer")
        sys.exit()
    if os.path.exists(outfile):
        print(f"{prog}: error: output file '{outfile}' exists")
        sys.exit()
    print(f"   + command line: count = {count}, outfile = '{outfile}'") 
    
    # create 'count' city locations and store them in an array
    # each location is a 2-tuple of x and y coordinate from 
    # the range [0,1]. To avoid (near) duplicates, a new city
    # is only accepted if its distance from all other cities
    # is at least 0.01.
    #
    # NOTE: TSM is scale invariant, i.e. scaling the unit length
    #       by a factor k does not affect the solution, and only
    #       scales the minimal length by the factor k. We thus
    #       restrict the x and y coordinates to the unit square.
    print(f"   + creating random TSM problem of size {count}")
    cities = []
    num  = 0
    while num < count : 
        x = random.uniform(0.01, 0.99)
        y = random.uniform(0.01, 0.99)
        succ = True
        for c in cities :
            d1 = c[0] - x;
            d2 = c[1] - y;
            d = math.sqrt(d1*d1 + d2*d2)
            if d < 0.01 : 
                succ = False
                break
        if succ :
            cities.append((x,y))
            num += 1
    
    # dump the array of city locations to the json output file
    print(f"   + writing TSM data to output file '{outfile}'")
    with open(outfile, 'w') as f:
        json.dump(cities, f, indent=2)
        
    # all done
    print("   + all done")
    return


# --------------------------------------------------------------------------
# run main() as a script only, not when importing this file as a module
# --------------------------------------------------------------------------

if __name__ == "__main__":
    main()
