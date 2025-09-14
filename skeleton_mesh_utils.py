import numpy as np

class rectangular_mesh:

    # class constructor

    def __init__(self, nx, lx, ny, ly):

        self.nx = nx # save nx into class
        self.lx = lx # save lx into class
        self.ny = ny # save ny into class
        self.ly = ly # save ly into class

        # generate mesh
        self.x = # your x array
        self.y = # your y array

        # calculate mesh resolution
        self.dx = # your x resolution
        self.dy = # your y resolution


    #######################################################################################################

    def get_mem_pos(self, ix, iy):
        """This function converts a pair of indices ix, iy to the memory index ik"""
        # notice that input arguments ix, iy follow Python notation - which is, they start from 0
        # (of course, output argument does the same)

        ik = # your expression

        return ik


    #######################################################################################################

    def get_mat_pos(self, ik):
        """This function converts a memory index ik to a pair of indices ix, iy.
        It is inverse to get_mem_pos."""

        ix = # your expression
        iy = # your expression

        return ix, iy


    #######################################################################################################

    def get_compass(self, curr_p):
        """This function returns the memory position of the (north, south, west, east) neighbors given
        a memory position ik. Note that the result may be incorrect at the boundary."""


        north = # position of northern neighbour
        south = # position of southern neighbour
        west = # position of western neighbour
        east = # position of eastern neighbour

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

        # initialise variables
        boundary = ''
        nout = ik # well, you basically never need to change this
        nin = None # point inside the domain that defines the normal direction to the boundary
        dn = None # = dx if on the western or eastern boundaries, = dy otherwise

        # boundary will be empty if the point is not on the boundary;
        # otherwise, it will contain one or more letters specifying on which boundary it is located

        # ...

        # assess: west or east
        if : # on the western boundary
            boundary += 'w'
            nin = #
            dn = #
        elif # on the eastern boundary
            boundary += 'e'
            nin = #
            dn = #

        # assess: north or south
        if # on the southern boundary
            boundary += 's'
            nin = #
            dn = #
        elif # on the northern boundary
            boundary += 'n'
            nin = #
            dn = #

        return boundary, nout, nin, dn