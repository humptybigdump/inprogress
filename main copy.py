import numpy as np
import sys

sys.path.append(".")

from project_fem.fem.interface.fenics_interface_solved import FenicsInterface


if __name__ == "__main__":

    # Create a FenicsInterface object
    #   This is the main interface to the Fenics library
    #   It handles the setup of the problem, the mesh generation,
    #   the assembly of the system matrices and vectors,
    #   and the solution of the system
    fi = FenicsInterface()
    fi.VERBOSITY = 2
    fi.DEBUG = False
    fi.plot = True

    # Define geometry, material properties, and boundary conditions
    geometry = [1.0, 1.0]  # Length in x and y directions

    # Define material properties
    #    Bilinear elastoplastic material with kinematic hardening
    E = 7e10  # Young's modulus
    nu = 0.3  # Poisson's ratio
    rho = 0.0  # Density
    sig0 = 2.50e8  # Yield stress
    Et = 1e-9  # Hardening modulus
    material = [E, nu, rho, sig0, Et]

    # Define properties
    thickness = 1.0  # Thickness of the material
    properties = [thickness]

    # Define boundary conditions
    #    At the left and right edges of the cube, we apply linear bending displacements.
    #    The displacements are defined as a function of the y coordinate.
    #    The maximum displacement is defined as u0.
    u0 = 3.5e-3  # MaximumDisplacement in y direction

    def lin_pos_y(node, max_val, **kwargs):
        val = max_val * 2.0 * (node[2] - geometry[1] / 2.0) / geometry[1]
        return val

    lin_pos_y.cpp_code = "max_val * (x[1] - geometry1 / 2.0) " "* (2.0 / geometry1)"

    def lin_neg_y(node, max_val, **kwargs):
        val = lin_pos_y(node, max_val)
        return -val

    lin_neg_y.cpp_code = "- max_val * (x[1] - geometry1 / 2.0) " "* (2.0 / geometry1)"

    bc_u1 = dict()
    bc_u1["xn"] = [lin_pos_y, None]  # Left edge
    bc_u1["xp"] = [lin_neg_y, None]  # Right edge
    bc_u1["yn"] = []  # Bottom edge
    bc_u1["yp"] = []  # Top edge
    bc_u1["all"] = []
    bc_u1["pointwise"] = []
    bc_f1 = None
    fi.bc_fun_kwargs = {"max_val": u0, "unit_disp": 0.0, "coords": None}

    # Finite element settings
    grid_shape = [27, 27]  # Number of elements in x and y directions
    fi.interpolation_order = 2  # element interpolation order (1: linear, 2: quadratic)
    fi.min_increment = 5  # Minimum number of time increments
    fi.max_iteration = 100  # Maximum number of iterations
    fi.tol = 1e-10  # Tolerance for convergence
    fi.regularization = 1.0  # Regularization parameter

    fe_histories = []  # List to store the finite element histories

    # Load the geometry
    print("Loading geometry...")
    fe_history_load = fi.adaptive_time_increments(
        fi.elastoplastic_cube,
        geometry,
        material,
        properties,
        grid_shape,
        bc_u1,
    )
    fe_histories += [fe_history_load]

    # Unload the geometry fully
    print("Unloading geometry...")
    remaining_load_factor = 0.0
    bc_u2 = fi.scale_boundary_conditions(
        fe_history_load[-1]["bc_u"], remaining_load_factor
    )
    # Unload
    fe_history_unload = fi.adaptive_time_increments(
        fi.elastoplastic_cube,
        geometry,
        material,
        properties,
        grid_shape,
        bc_u2,
        fe_state=fe_history_load[-1],  # Last frame of the loaded state
    )
    fe_histories += [fe_history_unload]

    # Extract results in fully loaded state
    fe_state1 = fe_histories[0][-1]  # Last frame
    xe1 = fe_state1["Xi"]  # Coordinates of the elements
    ue1 = fe_state1["Ui"]  # Displacements of the elements
    se1 = fe_state1["Si"]  # Stress of the elements
    fe1 = fe_state1["Fi"]  # Forces of the elements
    sig_mises1 = fi.extract_stress_values(se1, stress_type="mises")  # von Mises stress

    # Extract results in fully unloaded state
    fe_state2 = fe_histories[1][-1]  # Last frame
    xe2 = fe_state2["Xi"]  # Coordinates of the elements
    ue2 = fe_state2["Ui"]  # Displacements of the elements
    se2 = fe_state2["Si"]  # Stress of the elements
    fe2 = fe_state2["Fi"]  # Forces of the elements
    sig_mises2 = fi.extract_stress_values(se2, stress_type="mises")  # von Mises stress

    # Check geometry
    assert np.abs(np.max(xe1) - np.max(geometry)) < fi.tol
    # Check displacements
    assert np.abs(np.max(ue1) - u0) < fi.tol
    # Check stresses
    assert np.max(sig_mises1) > 0.0
    assert np.max(sig_mises1) <= sig0 * (1.0 + 1e-4)
