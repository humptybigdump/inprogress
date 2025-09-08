##**************************************************************************
# @file     lecture/src/app/ca.py
# @brief    cellular automaton in 1D
# @author   Markus Quandt  \n<markus.quandt@uni-tuebingen.de>
# *************************************************************************/

import numpy as np
import matplotlib; matplotlib.use('TkAgg')   # must be called before matplotlib.pyplot
import matplotlib.pyplot as plt


def advance(z, r):
    """Advance the configuration z by one time step according to rule r.

    Args:
        z (np.array): The current configuration of the CA (array of bits; each bit stored in uint8)
        r (np.uint8): The local transition rule, possible values are 0...255
        Return      : a copy of z advanced one time step by the CA rule
    """
    if len(z) < 3 :
        raise ValueError("Current CA state too small; need at least three cells.")
    zz = np.zeros_like(z)
    for i in range(len(z)):
        a = z[i-1] if i > 0 else z[-1]
        b = z[i]
        c = z[i+1] if i < len(z)-1 else z[0]
        n = a*4 + b*2 + c
        mask = 2**n
        zz[i] = ((r & mask) != 0)
    return zz


def init(z, p=None):
    """Initialize the configuration z with all 0's and a single 1 at position p

    Args:
        z (np.array): The configuration to inizialize (array of bits; each bit stored in uint8)
        pos (p, optional): Position of the set bit; must be in the range 0..len(z)-1. 
                           If p=None (the default), the position is chosen at random.
    """
    z.fill(0)
    if p == None : 
        pos = np.random.randint(0,len(z))
        z[pos] = np.uint8(1)
    else:
        if p < 0 or p >= len(z) : 
            raise ValueError("Init position out of range")
        z[p] = np.uint8(1)


def plot(out, rule) :
    """Plot a visualization of the current CA state with time running from bottom to top
    Args:
        out (list)     : Time sequence of states (increasing index is increasing time)        
        rule (np.uint8): The local transition rule, possible values are 0...255
    """
    data = np.row_stack( out )
    plt.xlabel("cell #")
    plt.ylabel("time")
    plt.legend(title=f"Rule: {rule}", loc="lower right")
    plt.imshow(data, cmap='tab20c_r', interpolation='nearest', origin='lower')
    plt.show(block=True)
      
    
def main():
    """The main entry point"""
    rule = 110                        # the CA local transition function
    L = 1200                          # number of cells in the CA
    L2 = int(L / 2)                   # half the size of the universe
    z = np.zeros(L, dtype=np.uint8)   # create cells
    init(z, L2)                       # initial state
    out = list()                      # stores time sequence of states
    for t in range(L2):               # iterate over time steps
        out.append(z)                 # store state at time t
        z = advance(z, rule)          # advance on time step 
    plot(out, rule)                   # plot the time sequence of states                
    
# guard: run main() only on direct execution, not on import
if __name__ == "__main__":
    main()