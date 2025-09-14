import copy as copy
import numpy as np

from functools import partial
from . import constants as c


def normal(loc=0.0, scale=1.0, size=None):
    """Compatibility to ABAQUS' numpy 1.6."""
    if scale > 0.0:
        return np.random.normal(loc=loc, scale=scale, size=size)
    else:
        if not size:
            return 0.0
        else:
            return np.zeros(shape=size, dtype=np.float)


def randomize_bc_u(
    geometry, loading_modes_value_std, craig_bampton_node=None, max_poly_degree=3
):
    """Define random boundary conditions from loading and rigid body modes.

    Args:
        geometry:                   meta element geometrical size
        loading_modes_value_std:    selected loading modes for randomization
        max_poly_degree:    maximum degree of polynomial for poly loading

    Returns:
        bc_u:       dict of iterables for dirichlet loading modes
                                [] or None: no bc
                                [0.0, None, 1.0]: fixed in x, free in y,
                                                  prescribed disp in z (3D)
        loading_mode:      randomly sampled loading mode for this sample
    """

    num_dims = len(geometry)

    # Select modes
    loading_mode = 0
    rigid_body_mode = 0

    assert isinstance(loading_modes_value_std, dict)
    loading_modes = list(loading_modes_value_std.keys())

    while not (loading_mode or rigid_body_mode):
        idx = np.random.randint(0, len(loading_modes))
        loading_mode = loading_modes[idx]

    # Get standard deviation of the boundary value
    bc_value_std = loading_modes_value_std[loading_mode]

    # Reduce max polynomial degree for multi-axial loading
    if loading_mode in [c.POLY_TRI, c.POLY_BI_XY, c.POLY_BI_YZ, c.POLY_BI_ZX]:
        max_poly_degree = 1

    # Loading modes
    u_bc_xn = []
    u_bc_xp = []
    u_bc_yp = []
    u_bc_yn = []
    u_bc_zp = []
    u_bc_zn = []
    u_bc_all = []
    u_bc_pointwise = []

    # Distribution functions
    def lin_pos_x(node, max_val, **kwargs):
        val = max_val * 2.0 * (node[1] - geometry[0] / 2.0) / geometry[0]
        return val

    lin_pos_x.cpp_code = "max_val * (x[0] - geometry0 / 2.0) " "* (2.0 / geometry0)"

    def lin_neg_x(**kwargs):
        val = lin_pos_x(**kwargs)
        return -val

    lin_neg_x.cpp_code = "- max_val * (x[0] - geometry0 / 2.0) " "* (2.0 / geometry0)"

    def lin_pos_y(node, max_val, **kwargs):
        val = max_val * 2.0 * (node[2] - geometry[1] / 2.0) / geometry[1]
        return val

    lin_pos_y.cpp_code = "max_val * (x[1] - geometry1 / 2.0) " "* (2.0 / geometry1)"

    def lin_neg_y(**kwargs):
        val = lin_pos_y(**kwargs)
        return -val

    lin_neg_y.cpp_code = "- max_val * (x[1] - geometry1 / 2.0) " "* (2.0 / geometry1)"

    def lin_pos_z(node, max_val, **kwargs):
        val = max_val * 2.0 * (node[3] - geometry[2] / 2.0) / geometry[2]
        return val

    lin_pos_z.cpp_code = "max_val * (x[2] - geometry2 / 2.0) " "* (2.0 / geometry2)"

    def lin_neg_z(**kwargs):
        val = lin_pos_y(**kwargs)
        return -val

    lin_neg_z.cpp_code = "- max_val * (x[2] - geometry2 / 2.0) " "* (2.0 / geometry2)"

    def quad_pos_x(node, max_val, **kwargs):
        s = (node[1] - geometry[0] / 2.0) / (geometry[0] / 2.0)
        return max_val * (s**2.0)

    def quad_neg_x(**kwargs):
        return -quad_pos_x(**kwargs)

    def quad_pos_y(node, max_val, **kwargs):
        s = (node[2] - geometry[1] / 2.0) / (geometry[1] / 2.0)
        return max_val * (s**2.0)

    def quad_neg_y(**kwargs):
        return -quad_pos_y(**kwargs)

    def quad_pos_z(node, max_val, **kwargs):
        s = (node[3] - geometry[2] / 2.0) / (geometry[2] / 2.0)
        return max_val * (s**2.0)

    def quad_neg_z(**kwargs):
        return -quad_pos_z(**kwargs)

    def cube_pos_x(node, max_val, **kwargs):
        s = (node[1] - geometry[0] / 2.0) / (geometry[0] / 2.0)
        return max_val * (s**3.0)

    def cube_neg_x(**kwargs):
        return -cube_pos_x(**kwargs)

    def cube_pos_y(node, max_val, **kwargs):
        s = (node[2] - geometry[1] / 2.0) / (geometry[1] / 2.0)
        return max_val * (s**3.0)

    def cube_neg_y(**kwargs):
        return -cube_pos_y(**kwargs)

    def cube_pos_z(node, max_val, **kwargs):
        s = (node[3] - geometry[2] / 2.0) / (geometry[2] / 2.0)
        return max_val * (s**3.0)

    def cube_neg_z(**kwargs):
        return -cube_pos_z(**kwargs)

    def poly(
        node, max_val=None, coefficients=None, direction=0, multiplier=1.0, **kwargs
    ):
        s = (node[direction + 1] - geometry[direction] / 2.0) / (
            geometry[direction] / 2.0
        )
        if coefficients is None and isinstance(max_val, float):
            coefficients = [max_val]
        coeff_multipliers = np.asarray([0.3, 0.3, 1.0, 1.0])
        coeff_multipliers = coeff_multipliers[-len(coefficients) :]
        coeff_multipliers = coeff_multipliers / np.sum(coeff_multipliers)
        coeff = coefficients * coeff_multipliers
        return multiplier * np.polyval(coeff, s)

    def craig_bampton(node, bcx, unit_disp, **kwargs):
        val = np.allclose(node[1:], bcx) * unit_disp
        return val

    craig_bampton.cpp_code = "(near(x[0], bcx0) && near(x[1], bcx1)) * unit_disp"

    # def rotate_x_val_y(node, max_val):
    #     yc = node[2] - geometry[1] / 2.0
    #     zc = node[3] - geometry[2] / 2.0
    #     cosa = np.cos(max_val)
    #     sina = np.sin(max_val)
    #     valy = (cosa - 1.0) * yc - sina * zc
    #     return valy
    #
    # def rotate_x_val_z(node, max_val):
    #     yc = node[2] - geometry[1] / 2.0
    #     zc = node[3] - geometry[2] / 2.0
    #     cosa = np.cos(max_val)
    #     sina = np.sin(max_val)
    #     valz = sina * yc + (cosa - 1.0) * zc
    #     return valz
    #
    # def rotate_y_val_x(node, max_val):
    #     xc = node[1] - geometry[0] / 2.0
    #     zc = node[3] - geometry[2] / 2.0
    #     cosa = np.cos(max_val)
    #     sina = np.sin(max_val)
    #     valx = (cosa - 1.0) * xc + sina * zc
    #     return valx
    #
    # def rotate_y_val_z(node, max_val):
    #     xc = node[1] - geometry[0] / 2.0
    #     zc = node[3] - geometry[2] / 2.0
    #     cosa = np.cos(max_val)
    #     sina = np.sin(max_val)
    #     valz = - sina * xc + (cosa - 1.0) * zc
    #     return valz
    #
    # def rotate_z_val_x(node, max_val):
    #     xc = node[1] - geometry[0] / 2.0
    #     yc = node[2] - geometry[1] / 2.0
    #     cosa = np.cos(max_val)
    #     sina = np.sin(max_val)
    #     valx = (cosa - 1.0) * xc - sina * yc
    #     return valx
    #
    # def rotate_z_val_y(node, max_val):
    #     xc = node[1] - geometry[0] / 2.0
    #     yc = node[2] - geometry[1] / 2.0
    #     cosa = np.cos(max_val)
    #     sina = np.sin(max_val)
    #     valy = sina * xc + (cosa - 1.0) * yc
    #     return valy

    # Define loading boundary conditions
    if loading_mode == DISABLED:
        pass
    elif loading_mode == c.UNI_X:
        # tensile/compression uniaxial x
        u_bc_xp = [normal(0.0, bc_value_std), None, None]
        u_bc_xn = [-normal(0.0, bc_value_std), None, None]
    elif loading_mode == c.UNI_Y:
        # tensile/compression uniaxial y
        assert num_dims > 1
        u_bc_yp = [None, normal(0.0, bc_value_std), None]
        u_bc_yn = [None, -normal(0.0, bc_value_std), None]
    elif loading_mode == c.UNI_Z:
        # tensile/compression uniaxial z
        assert num_dims > 2
        u_bc_zp = [None, None, normal(0.0, bc_value_std)]
        u_bc_zn = [None, None, -normal(0.0, bc_value_std)]
    elif loading_mode == c.BI_XY:
        # tensile/compression biaxial xy
        assert num_dims > 1
        u_bc_xp = [normal(0.0, bc_value_std), None, None]
        u_bc_xn = [-normal(0.0, bc_value_std), None, None]
        u_bc_yp = [None, normal(0.0, bc_value_std), None]
        u_bc_yn = [None, -normal(0.0, bc_value_std), None]
    elif loading_mode == c.BI_YZ:
        # tensile/compression biaxial yz
        assert num_dims > 2
        u_bc_yp = [None, normal(0.0, bc_value_std), None]
        u_bc_yn = [None, -normal(0.0, bc_value_std), None]
        u_bc_zp = [None, None, normal(0.0, bc_value_std)]
        u_bc_zn = [None, None, -normal(0.0, bc_value_std)]
    elif loading_mode == c.BI_ZX:
        # tensile/compression biaxial zx
        assert num_dims > 2
        u_bc_zp = [None, None, normal(0.0, bc_value_std)]
        u_bc_zn = [None, None, -normal(0.0, bc_value_std)]
        u_bc_xp = [normal(0.0, bc_value_std), None, None]
        u_bc_xn = [-normal(0.0, bc_value_std), None, None]
    elif loading_mode == c.TRI:
        # tensile/compression triaxial xyz
        assert num_dims > 2
        u_bc_xp = [normal(0.0, bc_value_std), None, None]
        u_bc_xn = [-normal(0.0, bc_value_std), None, None]
        u_bc_yp = [None, normal(0.0, bc_value_std), None]
        u_bc_yn = [None, -normal(0.0, bc_value_std), None]
        u_bc_zp = [None, None, normal(0.0, bc_value_std)]
        u_bc_zn = [None, None, -normal(0.0, bc_value_std)]
    elif loading_mode == c.SHEAR_XY:
        # shear xy
        assert num_dims > 1
        u_bc_xp = [None, normal(0.0, bc_value_std), None]
        u_bc_xn = [None, -normal(0.0, bc_value_std), None]
        u_bc_yp = [normal(0.0, bc_value_std), None, None]
        u_bc_yn = [-normal(0.0, bc_value_std), None, None]
    elif loading_mode == c.SHEAR_YZ:
        # shear yz
        assert num_dims > 2
        u_bc_yp = [None, None, normal(0.0, bc_value_std)]
        u_bc_yn = [None, None, -normal(0.0, bc_value_std)]
        u_bc_zp = [None, normal(0.0, bc_value_std), None]
        u_bc_zn = [None, -normal(0.0, bc_value_std), None]
    elif loading_mode == c.SHEAR_ZX:
        # shear zx
        assert num_dims > 2
        u_bc_zp = [normal(0.0, bc_value_std), None, None]
        u_bc_zn = [-normal(0.0, bc_value_std), None, None]
        u_bc_xp = [None, None, normal(0.0, bc_value_std)]
        u_bc_xn = [None, None, -normal(0.0, bc_value_std)]
    elif loading_mode == c.SHEAR2_XY:
        # quadratic shear xy
        assert num_dims > 1
        u_bc_xp = [None, quad_pos_y, None]
        u_bc_xn = [None, quad_neg_y, None]
        u_bc_yp = [quad_pos_x, None, None]
        u_bc_yn = [quad_neg_x, None, None]
    elif loading_mode == c.SHEAR2_YZ:
        # quadratic shear yz
        assert num_dims > 2
        u_bc_yp = [None, None, quad_pos_z]
        u_bc_yn = [None, None, quad_neg_z]
        u_bc_zp = [None, quad_pos_y, None]
        u_bc_zn = [None, quad_neg_y, None]
    elif loading_mode == c.SHEAR2_ZX:
        # quadratic shear zx
        assert num_dims > 2
        u_bc_zp = [quad_pos_x, None, None]
        u_bc_zn = [quad_neg_x, None, None]
        u_bc_xp = [None, None, quad_pos_z]
        u_bc_xn = [None, None, quad_neg_z]
    elif loading_mode == c.BEND_XY:
        # bending x boundary around z axis
        assert num_dims > 1
        u_bc_xp = [lin_pos_y, None, None]
        u_bc_xn = [lin_neg_y, None, None]
    elif loading_mode == c.BEND_YX:
        # bending y boundary around z axis
        assert num_dims > 1
        u_bc_yp = [None, lin_pos_x, None]
        u_bc_yn = [None, lin_neg_x, None]
    elif loading_mode == c.BEND_YZ:
        # bending y boundary around x axis
        assert num_dims > 2
        u_bc_yp = [None, lin_pos_z, None]
        u_bc_yn = [None, lin_neg_z, None]
    elif loading_mode == c.BEND_ZY:
        # bending z boundary around x axis
        assert num_dims > 2
        u_bc_zp = [None, None, lin_pos_y]
        u_bc_zn = [None, None, lin_neg_y]
    elif loading_mode == c.BEND_ZX:
        # bending z boundary around y axis
        assert num_dims > 2
        u_bc_zp = [None, None, lin_pos_x]
        u_bc_zn = [None, None, lin_neg_x]
    elif loading_mode == c.BEND_XZ:
        # bending x boundary around y axis
        assert num_dims > 2
        u_bc_xp = [lin_neg_z, None, None]
        u_bc_xn = [lin_pos_z, None, None]
    elif loading_mode == c.POLY_UNI_X:
        # polynomial uniaxial x
        coeff_pos = normal(0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2))
        coeff_neg = normal(0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2))
        direction = 1
        # TODO: direction 2 may vary too in 3D
        pos_fun = partial(
            poly, coefficients=coeff_pos, multiplier=1.0, direction=direction
        )
        neg_fun = partial(
            poly, coefficients=coeff_neg, multiplier=-1.0, direction=direction
        )
        u_bc_xp = [pos_fun, None, None]
        u_bc_xn = [neg_fun, None, None]
    elif loading_mode == c.POLY_UNI_Y:
        # polynomial uniaxial y
        assert num_dims > 1
        coeff_pos = normal(0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2))
        coeff_neg = normal(0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2))
        direction = 0
        # TODO: direction 2 may vary too in 3D
        pos_fun = partial(
            poly, coefficients=coeff_pos, multiplier=1.0, direction=direction
        )
        neg_fun = partial(
            poly, coefficients=coeff_neg, multiplier=-1.0, direction=direction
        )
        u_bc_yp = [None, pos_fun, None]
        u_bc_yn = [None, neg_fun, None]
    elif loading_mode == c.POLY_UNI_Z:
        # polynomial uniaxial z
        assert num_dims > 2
        coeff_pos = normal(0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2))
        coeff_neg = normal(0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2))
        direction = 0
        # TODO: direction 1 may vary too in 3D
        pos_fun = partial(
            poly, coefficients=coeff_pos, multiplier=1.0, direction=direction
        )
        neg_fun = partial(
            poly, coefficients=coeff_neg, multiplier=-1.0, direction=direction
        )
        u_bc_zp = [None, None, pos_fun]
        u_bc_zn = [None, None, neg_fun]
    elif loading_mode == c.POLY_BI_XY:
        # polynomial biaxial xy
        assert num_dims > 1
        coeff_pos0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction0 = 1
        # TODO: direction 2 may vary too
        pos_fun0 = partial(
            poly, coefficients=coeff_pos0, multiplier=1.0, direction=direction0
        )
        neg_fun0 = partial(poly, coefficients=coeff_neg0, direction=direction0)
        coeff_pos1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction1 = 0
        # TODO: direction 2 may vary too
        pos_fun1 = partial(
            poly, coefficients=coeff_pos1, multiplier=1.0, direction=direction1
        )
        neg_fun1 = partial(poly, coefficients=coeff_neg1, direction=direction1)
        u_bc_xp = [pos_fun0, None, None]
        u_bc_xn = [neg_fun0, None, None]
        u_bc_yp = [None, pos_fun1, None]
        u_bc_yn = [None, neg_fun1, None]
    elif loading_mode == c.POLY_BI_YZ:
        # polynomial biaxial yz
        assert num_dims > 2
        coeff_pos0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction0 = 2
        # TODO: direction 0 may vary too
        pos_fun0 = partial(
            poly, coefficients=coeff_pos0, multiplier=1.0, direction=direction0
        )
        neg_fun0 = partial(poly, coefficients=coeff_neg0, direction=direction0)
        coeff_pos1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction1 = 1
        # TODO: direction 0 may vary too
        pos_fun1 = partial(
            poly, coefficients=coeff_pos1, multiplier=1.0, direction=direction1
        )
        neg_fun1 = partial(poly, coefficients=coeff_neg1, direction=direction1)
        u_bc_yp = [None, pos_fun0, None]
        u_bc_yn = [None, neg_fun0, None]
        u_bc_zp = [None, None, pos_fun1]
        u_bc_zn = [None, None, neg_fun1]
    elif loading_mode == c.POLY_BI_ZX:
        # polynomial biaxial zx
        assert num_dims > 2
        coeff_pos0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction0 = 0
        # TODO: direction 1 may vary too
        pos_fun0 = partial(
            poly, coefficients=coeff_pos0, multiplier=1.0, direction=direction0
        )
        neg_fun0 = partial(poly, coefficients=coeff_neg0, direction=direction0)
        coeff_pos1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction1 = 2
        # TODO: direction 1 may vary too
        pos_fun1 = partial(
            poly, coefficients=coeff_pos1, multiplier=1.0, direction=direction1
        )
        neg_fun1 = partial(poly, coefficients=coeff_neg1, direction=direction1)
        u_bc_zp = [None, None, pos_fun0]
        u_bc_zn = [None, None, neg_fun0]
        u_bc_xp = [pos_fun1, None, None]
        u_bc_xn = [neg_fun1, None, None]
    elif loading_mode == c.POLY_TRI:
        # polynomial triaxial xyz
        assert num_dims > 2
        coeff_pos0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg0 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction0 = 2
        # TODO: direction 1 may vary too
        pos_fun0 = partial(
            poly, coefficients=coeff_pos0, multiplier=1.0, direction=direction0
        )
        neg_fun0 = partial(poly, coefficients=coeff_neg0, direction=direction0)
        coeff_pos1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg1 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction1 = 0
        # TODO: direction 2 may vary too
        pos_fun1 = partial(
            poly, coefficients=coeff_pos1, multiplier=1.0, direction=direction1
        )
        neg_fun1 = partial(poly, coefficients=coeff_neg1, direction=direction1)
        coeff_pos2 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        coeff_neg2 = normal(
            0.0, bc_value_std, np.random.randint(1, max_poly_degree + 2)
        )
        direction2 = 0
        # TODO: direction 1 may vary too
        pos_fun2 = partial(
            poly, coefficients=coeff_pos2, multiplier=1.0, direction=direction2
        )
        neg_fun2 = partial(poly, coefficients=coeff_neg2, direction=direction2)
        u_bc_xp = [pos_fun0, None, None]
        u_bc_xn = [neg_fun0, None, None]
        u_bc_yp = [None, pos_fun1, None]
        u_bc_yn = [None, neg_fun1, None]
        u_bc_zp = [None, None, pos_fun2]
        u_bc_zn = [None, None, neg_fun2]
    elif loading_mode == c.POLY_SHEAR_XY:
        # polynomial shear xy
        assert num_dims > 1
        signs = np.sign(normal(0.0, 1.0, max_poly_degree + 2))
        coeff_pos0 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_neg0 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_pos1 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_neg1 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_pos0 *= signs
        coeff_neg0 *= -signs
        coeff_pos1 *= signs
        coeff_neg1 *= -signs
        coeff_pos0 = coeff_pos0[: np.random.randint(1, max_poly_degree + 2)]
        coeff_neg0 = coeff_neg0[: np.random.randint(1, max_poly_degree + 2)]
        coeff_pos1 = coeff_pos1[: np.random.randint(1, max_poly_degree + 2)]
        coeff_neg1 = coeff_neg1[: np.random.randint(1, max_poly_degree + 2)]
        direction0 = 1
        # TODO: direction 2 may vary too
        pos_fun0 = partial(poly, coefficients=coeff_pos0, direction=direction0)
        neg_fun0 = partial(poly, coefficients=coeff_neg0, direction=direction0)
        direction1 = 0
        # TODO: direction 2 may vary too
        pos_fun1 = partial(poly, coefficients=coeff_pos1, direction=direction1)
        neg_fun1 = partial(poly, coefficients=coeff_neg1, direction=direction1)
        u_bc_xp = [None, pos_fun0, None]
        u_bc_xn = [None, neg_fun0, None]
        u_bc_yp = [pos_fun1, None, None]
        u_bc_yn = [neg_fun1, None, None]
    elif loading_mode == c.POLY_SHEAR_YZ:
        # polynomial shear yz
        assert num_dims > 2
        signs = np.sign(normal(0.0, 1.0, max_poly_degree + 2))
        coeff_pos0 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_neg0 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_pos1 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_neg1 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_pos0 *= signs
        coeff_neg0 *= -signs
        coeff_pos1 *= signs
        coeff_neg1 *= -signs
        coeff_pos0 = coeff_pos0[: np.random.randint(1, max_poly_degree + 2)]
        coeff_neg0 = coeff_neg0[: np.random.randint(1, max_poly_degree + 2)]
        coeff_pos1 = coeff_pos1[: np.random.randint(1, max_poly_degree + 2)]
        coeff_neg1 = coeff_neg1[: np.random.randint(1, max_poly_degree + 2)]
        direction0 = 1
        # TODO: direction 2 may vary too
        pos_fun0 = partial(poly, coefficients=coeff_pos0, direction=direction0)
        neg_fun0 = partial(poly, coefficients=coeff_neg0, direction=direction0)
        direction1 = 0
        # TODO: direction 2 may vary too
        pos_fun1 = partial(poly, coefficients=coeff_pos1, direction=direction1)
        neg_fun1 = partial(poly, coefficients=coeff_neg1, direction=direction1)
        u_bc_yp = [None, None, pos_fun0]
        u_bc_yn = [None, None, neg_fun0]
        u_bc_zp = [None, pos_fun1, None]
        u_bc_zn = [None, neg_fun1, None]
    elif loading_mode == c.POLY_SHEAR_ZX:
        # polynomial shear zx
        assert num_dims > 2
        signs = np.sign(normal(0.0, 1.0, max_poly_degree + 2))
        coeff_pos0 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_neg0 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_pos1 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_neg1 = np.abs(normal(0.0, bc_value_std, max_poly_degree + 2))
        coeff_pos0 *= signs
        coeff_neg0 *= -signs
        coeff_pos1 *= signs
        coeff_neg1 *= -signs
        coeff_pos0 = coeff_pos0[: np.random.randint(1, max_poly_degree + 2)]
        coeff_neg0 = coeff_neg0[: np.random.randint(1, max_poly_degree + 2)]
        coeff_pos1 = coeff_pos1[: np.random.randint(1, max_poly_degree + 2)]
        coeff_neg1 = coeff_neg1[: np.random.randint(1, max_poly_degree + 2)]
        direction0 = 1
        # TODO: direction 2 may vary too
        pos_fun0 = partial(poly, coefficients=coeff_pos0, direction=direction0)
        neg_fun0 = partial(poly, coefficients=coeff_neg0, direction=direction0)
        direction1 = 0
        # TODO: direction 2 may vary too
        pos_fun1 = partial(poly, coefficients=coeff_pos1, direction=direction1)
        neg_fun1 = partial(poly, coefficients=coeff_neg1, direction=direction1)
        u_bc_zp = [pos_fun0, None, None]
        u_bc_zn = [neg_fun0, None, None]
        u_bc_xp = [None, None, pos_fun1]
        u_bc_xn = [None, None, neg_fun1]
    elif loading_mode == c.CRAIG_BAMPTON_X:
        u_bc_all = [craig_bampton, 0.0, 0.0]
    elif loading_mode == c.CRAIG_BAMPTON_Y:
        assert num_dims > 1
        u_bc_all = [0.0, craig_bampton, 0.0]
    elif loading_mode == c.CRAIG_BAMPTON_Z:
        assert num_dims > 2
        u_bc_all = [0.0, 0.0, craig_bampton]
    elif loading_mode == c.ZERO:
        u_bc_all = [0.0, 0.0, 0.0]
    else:
        raise ValueError("Unknown loading mode: {:d}".format(loading_mode))

    bc_u = {
        "xp": u_bc_xp[:num_dims],
        "xn": u_bc_xn[:num_dims],
        "yp": u_bc_yp[:num_dims],
        "yn": u_bc_yn[:num_dims],
        "zp": u_bc_zp[:num_dims],
        "zn": u_bc_zn[:num_dims],
        "all": u_bc_all[:num_dims],
        "pointwise": u_bc_pointwise[:num_dims],
    }

    # # Rigid body modes
    # u_bc_rigid_x = []
    # u_bc_rigid_y = []
    # u_bc_rigid_z = []
    # u_bc_rigid_xy = []
    # u_bc_rigid_yz = []
    # u_bc_rigid_zx = []
    # u_bc_rigid_xyz = []
    # u_bc_rigid_rot_x = []
    # u_bc_rigid_rot_y = []
    # u_bc_rigid_rot_z = []
    #
    # if rigid_body_mode == DISABLED:
    #     pass
    # elif rigid_body_mode == RIGID_X:
    #     # rigid body motion x
    #     val_x = normal(0.0, rigid_body_std)
    #     u_bc_rigid_x = [val_x, None, None]
    # elif rigid_body_mode == RIGID_Y:
    #     # rigid body motion y
    #     assert num_dims > 1
    #     val_y = normal(0.0, rigid_body_std)
    #     u_bc_rigid_y = [None, val_y, None]
    # elif rigid_body_mode == RIGID_Z:
    #     # rigid body motion z
    #     assert num_dims > 2
    #     val_z = normal(0.0, rigid_body_std)
    #     u_bc_rigid_z = [None, None, val_z]
    # elif rigid_body_mode == RIGID_XY:
    #     # rigid body motion xy
    #     assert num_dims > 1
    #     val_x = normal(0.0, rigid_body_std)
    #     val_y = normal(0.0, rigid_body_std)
    #     u_bc_rigid_xy = [val_x, val_y, None]
    # elif rigid_body_mode == RIGID_YZ:
    #     # rigid body motion yz
    #     assert num_dims > 2
    #     val_y = normal(0.0, rigid_body_std)
    #     val_z = normal(0.0, rigid_body_std)
    #     u_bc_rigid_xy = [None, val_y, val_z]
    # elif rigid_body_mode == RIGID_ZX:
    #     # rigid body motion zx
    #     assert num_dims > 2
    #     val_z = normal(0.0, rigid_body_std)
    #     val_x = normal(0.0, rigid_body_std)
    #     u_bc_rigid_xy = [val_x, None, val_z]
    # elif rigid_body_mode == RIGID_XYZ:
    #     # rigid body motion zx
    #     assert num_dims > 2
    #     val = normal(0.0, rigid_body_std, [3])
    #     u_bc_rigid_xyz = val
    # elif rigid_body_mode == RIGID_ROT_X:
    #     # rotation around x axis
    #     assert num_dims > 2
    #     u_bc_rigid_rot_x = [None, rotate_x_val_y, rotate_x_val_z]
    # elif rigid_body_mode == RIGID_ROT_Y:
    #     # rotation around y axis
    #     assert num_dims > 2
    #     u_bc_rigid_rot_y = [rotate_y_val_x, None, rotate_y_val_z]
    # elif rigid_body_mode == RIGID_ROT_Z:
    #     # rotation around z axis
    #     assert num_dims > 1
    #     u_bc_rigid_rot_z = [rotate_z_val_x, rotate_z_val_y, None]
    # else:
    #     raise ValueError('Unknown rigid body mode: {:d}'.format(
    #         rigid_body_mode))
    #
    # U_bc_rigid_body = {'x': u_bc_rigid_x,
    #                    'y': u_bc_rigid_y,
    #                    'z': u_bc_rigid_z,
    #                    'xy': u_bc_rigid_xy,
    #                    'yz': u_bc_rigid_yz,
    #                    'zx': u_bc_rigid_zx,
    #                    'xyz': u_bc_rigid_xyz,
    #                    'rx': u_bc_rigid_rot_x,
    #                    'ry': u_bc_rigid_rot_y,
    #                    'rz': u_bc_rigid_rot_z}

    return bc_u, loading_mode


def randomize_params(
    size,
    material,
    properties,
    geom_noise_std=0.0,
    mat_noise_std=0.0,
    prop_noise_std=0.0,
):
    """Randomize geometry and material parameters."""
    # Copy
    size = copy.copy(size)
    material = copy.copy(material)
    properties = copy.copy(properties)
    # Randomize
    #   only operate on floats and ignore ints/dicts/lists/etc
    if geom_noise_std:
        size = [
            s * (1.0 + normal(0.0, geom_noise_std))
            for s in size
            if isinstance(s, float)
        ]
    if mat_noise_std:
        material = [
            m * (1.0 + normal(0.0, mat_noise_std))
            for m in material
            if isinstance(m, float)
        ]
    if prop_noise_std:
        properties = [
            p * (1.0 + normal(0.0, prop_noise_std))
            for p in properties
            if isinstance(p, float)
        ]
    return np.asarray(size), np.asarray(material), np.asarray(properties)


def _get_value(bc, *args, **kwargs):
    if bc:
        bc = [b if not callable(b) else b(*args, **kwargs) for b in bc]
        for b in bc:
            assert b is None or isinstance(b, float)
        return np.ma.array(bc, mask=(np.asarray(bc) == None), fill_value=0.0)
    else:
        return np.ma.array([0.0, 0.0], fill_value=0.0, mask=True)


def merge_bc_u(bc_u1, bc_u2, ratio=0.5):
    """Merge two boundary condition dictionaries."""
    corner_values = dict()
    # Get values at corners bc 1
    cnode = ["", 0.0, 0.0]
    ma1 = _get_value(bc_u1["xn"], cnode)
    mb1 = _get_value(bc_u1["yn"], cnode)
    corner_values["xn-yn1"] = np.ma.array(
        (1.0 - ratio) * ma1.filled() + (1.0 - ratio) * mb1.filled(),
        mask=(ma1.mask * mb1.mask),
    )
    cnode = ["", 1.0, 0.0]
    ma1 = _get_value(bc_u1["xp"], cnode)
    mb1 = _get_value(bc_u1["yn"], cnode)
    corner_values["xp-yn1"] = np.ma.array(
        (1.0 - ratio) * ma1.filled() + (1.0 - ratio) * mb1.filled(),
        mask=(ma1.mask * mb1.mask),
    )
    cnode = ["", 1.0, 1.0]
    ma1 = _get_value(bc_u1["xp"], cnode)
    mb1 = _get_value(bc_u1["yp"], cnode)
    corner_values["xp-yp1"] = np.ma.array(
        (1.0 - ratio) * ma1.filled() + (1.0 - ratio) * mb1.filled(),
        mask=(ma1.mask * mb1.mask),
    )
    cnode = ["", 0.0, 1.0]
    ma1 = _get_value(bc_u1["xn"], cnode)
    mb1 = _get_value(bc_u1["yp"], cnode)
    corner_values["xn-yp1"] = np.ma.array(
        (1.0 - ratio) * ma1.filled() + (1.0 - ratio) * mb1.filled(),
        mask=(ma1.mask * mb1.mask),
    )

    # Get values at corners bc2
    cnode = ["", 0.0, 0.0]
    ma2 = _get_value(bc_u2["xn"], cnode)
    mb2 = _get_value(bc_u2["yn"], cnode)
    corner_values["xn-yn2"] = np.ma.array(
        ratio * ma2.filled() + ratio * mb2.filled(), mask=(ma2.mask * mb2.mask)
    )
    cnode = ["", 1.0, 0.0]
    ma2 = _get_value(bc_u2["xp"], cnode)
    mb2 = _get_value(bc_u2["yn"], cnode)
    corner_values["xp-yn2"] = np.ma.array(
        ratio * ma2.filled() + ratio * mb2.filled(), mask=(ma2.mask * mb2.mask)
    )
    cnode = ["", 1.0, 1.0]
    ma2 = _get_value(bc_u2["xp"], cnode)
    mb2 = _get_value(bc_u2["yp"], cnode)
    corner_values["xp-yp2"] = np.ma.array(
        ratio * ma2.filled() + ratio * mb2.filled(), mask=(ma2.mask * mb2.mask)
    )
    cnode = ["", 0.0, 1.0]
    ma2 = _get_value(bc_u2["xn"], cnode)
    mb2 = _get_value(bc_u2["yp"], cnode)
    corner_values["xn-yp2"] = np.ma.array(
        ratio * ma2.filled() + ratio * mb2.filled(), mask=(ma2.mask * mb2.mask)
    )

    # Create consistency boundary conditions using linear interpolate functions
    def _lin_interpolate(node, minval=-1.0, maxval=1.0, direction=0, **kwargs):
        s = node[direction + 1]
        return (1.0 - s) * minval + s * maxval

    # Consistency boundary conditions on bc 1 from bc 2
    bc_consistency12 = dict()
    bc_consistency12["xn"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn2"][0],
            maxval=corner_values["xn-yp2"][0],
            direction=1,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn2"][1],
            maxval=corner_values["xn-yp2"][1],
            direction=1,
        ),
    ]
    bc_consistency12["xp"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xp-yn2"][0],
            maxval=corner_values["xp-yp2"][0],
            direction=1,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xp-yn2"][1],
            maxval=corner_values["xp-yp2"][1],
            direction=1,
        ),
    ]
    bc_consistency12["yn"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn2"][0],
            maxval=corner_values["xp-yn2"][0],
            direction=0,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn2"][1],
            maxval=corner_values["xp-yn2"][1],
            direction=0,
        ),
    ]
    bc_consistency12["yp"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yp2"][0],
            maxval=corner_values["xp-yp2"][0],
            direction=0,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yp2"][1],
            maxval=corner_values["xp-yp2"][1],
            direction=0,
        ),
    ]

    # Consistency boundary conditions on bc 2 from bc 1
    bc_consistency21 = dict()
    bc_consistency21["xn"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn1"][0],
            maxval=corner_values["xn-yp1"][0],
            direction=1,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn1"][1],
            maxval=corner_values["xn-yp1"][1],
            direction=1,
        ),
    ]
    bc_consistency21["xp"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xp-yn1"][0],
            maxval=corner_values["xp-yp1"][0],
            direction=1,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xp-yn1"][1],
            maxval=corner_values["xp-yp1"][1],
            direction=1,
        ),
    ]
    bc_consistency21["yn"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn1"][0],
            maxval=corner_values["xp-yn1"][0],
            direction=0,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yn1"][1],
            maxval=corner_values["xp-yn1"][1],
            direction=0,
        ),
    ]
    bc_consistency21["yp"] = [
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yp1"][0],
            maxval=corner_values["xp-yp1"][0],
            direction=0,
        ),
        partial(
            _lin_interpolate,
            minval=corner_values["xn-yp1"][1],
            maxval=corner_values["xp-yp1"][1],
            direction=0,
        ),
    ]

    # Merge both boundaries and consistency interpolate functions
    # all_keys = set(list(bc_u1.keys()) + list(bc_u2.keys()))
    bc_u = dict()
    for k in ["xn", "xp", "yn", "yp"]:  # TODO: Support for 3D, pointwise
        # Get constraints for current boundary
        try:
            bc1 = bc_u1[k]
        except KeyError:
            bc1 = [None, None]  # Unconstrained
        try:
            bc2 = bc_u2[k]
        except KeyError:
            bc2 = [None, None]  # Unconstrained
        try:
            bc12 = bc_consistency12[k]
            bc21 = bc_consistency21[k]
        except KeyError:
            raise ValueError("Cannot merge boundary condition of type: {:s}".format(k))
        # Merge to new boundary condition
        bc = []
        for c1, c2, cc12, cc21 in zip(bc1, bc2, bc12, bc21):

            # Turn absolute constraints into functions
            if c1 is not None and not callable(c1):
                c1 = lambda *args, **kwargs: c1
                assert isinstance(c1([0, 0.0, 1.0]), float)
            if c2 is not None and not callable(c2):
                c2 = lambda *args, **kwargs: c2
                assert isinstance(c2([0, 0.0, 1.0]), float)

            # Merge Function
            def merged_fun(
                *args, _c1=None, _c2=None, _cc12=None, _cc21=None, _ratio=0.5, **kwargs
            ):
                val = 0.0
                if _c1 is not None:
                    val += (1.0 - _ratio) * _c1(*args, **kwargs)
                    # Apply consistency bc from bc 2
                    if _cc12 is not None:
                        val += _cc12(*args, **kwargs)
                if _c2 is not None:
                    val += _ratio * _c2(*args, **kwargs)
                    # Apply consistency bc from bc 1
                    if _cc21 is not None:
                        val += _cc21(*args, **kwargs)
                return val

            # Merge
            if c1 is None and c2 is None:
                bc.append(None)
            else:
                bc.append(
                    partial(
                        merged_fun, _c1=c1, _c2=c2, _cc12=cc12, _cc21=cc21, _ratio=ratio
                    )
                )

        # Add to bc dictionary
        bc_u[k] = bc
    return bc_u


def _legacy_merge_bc_u(bc_u1, bc_u2, ratio=0.5):
    """Merge two boundary condition dictionaries."""
    all_keys = set(list(bc_u1.keys()) + list(bc_u2.keys()))
    bc_u = dict()
    for k in all_keys:
        # Get individual constrains
        try:
            constraint1 = bc_u1[k]
        except KeyError:
            # Key does not exist in dictionary so must be from other bc dict
            constraint1 = [None] * len(bc_u2.values()[0])
        try:
            constraint2 = bc_u2[k]
        except KeyError:
            # Key does not exist in dictionary so must be from other bc dict
            constraint2 = [None] * len(bc_u1.values()[0])
        if constraint1 and constraint2:
            # Merge constraints
            constraint = []
            for c1, c2 in zip(constraint1, constraint2):
                if isinstance(c1, float) and isinstance(c2, float):
                    # Two floats
                    constraint.append((1.0 - ratio) * c1 + ratio * c2)
                elif callable(c1) and callable(c2):
                    # Two functions

                    def merged_bc_fun(node, max_val, c1=c1, c2=c2, **kwargs):
                        return (1.0 - ratio) * c1(
                            node=node, max_val=max_val, **kwargs
                        ) + ratio * c2(node=node, max_val=max_val, **kwargs)

                    if hasattr(c1, "cpp_code"):
                        merged_bc_fun.cpp_code = (
                            "(1.0 - {:f}) * ({:s}) + {:f} * ({:s})".format(
                                ratio, c1.cpp_code, ratio, c2.cpp_code
                            )
                        )

                    constraint.append(merged_bc_fun)
                elif callable(c1) and isinstance(c2, float):
                    # Function and float

                    def merged_bc_fun(node, max_val, c1=c1, c2=c2, **kwargs):
                        return (1.0 - ratio) * c1(
                            node=node, max_val=max_val, **kwargs
                        ) + ratio * c2

                    if hasattr(c1, "cpp_code"):
                        merged_bc_fun.cpp_code = (
                            "(1.0 - {:f}) * ({:s}) + {:f} * {:f}".format(
                                ratio, c1.cpp_code, ratio, c2
                            )
                        )

                    constraint.append(merged_bc_fun)
                elif isinstance(c1, float) and callable(c2):
                    # Function and float

                    def merged_bc_fun(node, max_val, c1=c1, c2=c2, **kwargs):
                        return (1.0 - ratio) * c1 + ratio * c2(
                            node=node, max_val=max_val, **kwargs
                        )

                    if hasattr(c2, "cpp_code"):
                        merged_bc_fun.cpp_code = (
                            "(1.0 - {:f}) * {:f} + {:f} * ({:s})".format(
                                ratio, c1, ratio, c2.cpp_code
                            )
                        )
                    constraint.append(merged_bc_fun)
                elif c2 is None:
                    # Anything and None
                    constraint.append(c1)
                elif c1 is None:
                    # Anything and None
                    constraint.append(c2)
                else:
                    raise ValueError(
                        "Invalid combination of constraints: {:s}.".format(k)
                    )
        # The following fallback solutions ignore the secondary constraint, if
        #   the primary constraint is empty. This is necessary, e.g. for
        #   shearing and bending, since the unconstrained boundary must be
        #   able to move freely to avoid singularity at the corner. However,
        #   for combining uniaxial x and bi-axial xy loading, the biaxial
        #   mode must be primary, else one of its directions is forgotten.
        elif constraint1:
            # Secondary constraint empty
            constraint = constraint1
        elif constraint2:
            # Primary constraint empty
            constraint = []
        elif not (constraint1 or constraint2):
            constraint = []
        # Add constraint to dictionary
        bc_u[k] = constraint
    return bc_u
