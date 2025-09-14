import numpy as np

class rectangular_mesh:

    # class constructor

    def __init__(self, nx, lx, ny, ly):

        self.nx = nx # save nx into class
        self.lx = lx # save lx into class
        self.ny = ny # save ny into class
        self.ly = ly # save ly into class

        # generate mesh
        self.x = np.linspace(0, self.lx, self.nx)
        self.y = np.linspace(0, self.ly, self.ny)

        # calculate mesh resolution
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]


    #######################################################################################################

    def get_mem_pos(self, ix, iy):
        """This function converts a pair of indices ix, iy to the memory index ik"""
        # notice that input arguments ix, iy follow Python notation - which is, they start from 0

        ny = self.ny

        return ix*ny + iy


    #######################################################################################################

    def get_mat_pos(self, ik):
        """This function converts a memory index ik to a pair of indices ix, iy.
        It is inverse to get_mem_pos."""

        ny = self.ny

        ix = ik // ny
        iy = ik % ny

        return ix, iy


    #######################################################################################################

    def get_compass(self, ik): 
        """This function returns the memory position of the (north, south, west, east) neighbors given
        a memory position ik. Note that the result may be incorrect at the boundary."""

        north = ik + 1
        south = ik - 1
        west = ik - self.ny
        east = ik + self.ny

        return north, south, west, east


    #######################################################################################################


    def is_boundary(self, ik):
        """This function checks whether a point ik (in memory position) is on the boundary.
        Its purpose is to simplify the creation of a Neumann boundary condition.

        If so, it returns as Tuple:
          - boundary: 'n' for northern boundary, 'w' for western boundary, 'nw' for northwest corner etc.
          - nout, nin: the nodes required for a normal derivative at the boundary. nout is the current
            node (nout=ik), nin is the node adjacent to it and normal to the boundary 
          - dn: the denominator for the normal derivative, i.e. dx for n/s boundary or dy for w/e boundary
        If not, it returns '', ik, None, None.
        """
        ny = self.ny
        nx = self.nx

        # initialise variables
        boundary = ''
        nout = ik
        nin = None
        dn = None

        # boundary will be empty if the point is not on the boundary;
        # otherwise, it will contain one or more letters specifying on which boundary it is located

        # get the neighboring points
        north, south, west, east = self.get_compass(ik)

        # assess: west or east
        if ik < ny:
            boundary += 'w'
            nin = east
            dn = self.dx
        elif ik >= ny*(nx-1):
            boundary += 'e'
            nin = west
            dn = self.dx

        # assess: north or south
        if (ik % ny) == 0:
            boundary += 's'
            nin = north
            dn = self.dy
        elif (ik % ny) == (ny - 1):
            boundary += 'n'
            nin = south
            dn = self.dy

        return boundary, nout, nin, dn