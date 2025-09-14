import os
import sys
import shutil
import copy
import logging
import numpy as np
import matplotlib.pyplot as plt
import warnings
import colorama
import dolfin as fx

colorama.init()

from colorama import Fore, Back, Style
from tqdm.autonotebook import tqdm
from collections import OrderedDict
from ffc.quadrature.deprecation import QuadratureRepresentationDeprecationWarning

from ..base.grids import generate_grid
from ..base.random import normal
from ..base import errors
from .base_interface import BaseInterface


class FenicsInterface(BaseInterface):

    DEBUG = False

    def __init__(self, plot=False, write=False):
        """An interface for the fenics finite element solver.

        Args:
            plot:       optional: plot the result in a window
            write:      optional: write the result to a .pvd file
        """
        super(FenicsInterface, self).__init__(plot=plot, write=write)
        # Boundary conditions
        self.plane_stress = False
        # Fenics settings
        fx.parameters["form_compiler"]["cpp_optimize"] = True
        fx.parameters["form_compiler"]["optimize"] = True
        fx.parameters["form_compiler"]["representation"] = "uflacs"
        # fx.parameters['form_compiler']['representation'] = 'quadrature'
        # Rigid body motion variables
        self.urb = np.asarray([0.0, 0.0])
        self.Rrb = np.identity(2)
        self.constrained = np.asarray([False, False])
        self.report_stress_mode = "assert"  #'warn' #'write' # None
        self.return_initial_state = False
        # Disable logging
        if not self.DEBUG:
            fx.set_log_level(50)
            logging.getLogger("FFC").setLevel(logging.WARNING)
        # Disable warnings for using deprecated quadrature elements
        #   Needed for elastoplasticity
        warnings.simplefilter("ignore", QuadratureRepresentationDeprecationWarning)
        warnings.simplefilter("ignore", FutureWarning)
        if not self.DEBUG:
            warnings.filterwarnings(
                "ignore", "number of integration points for each cell"
            )
        # Store initial stiffness for plasticity
        self.A0 = None
        # # Clean Cache
        # self.clean_cache()

    def report(self, msg):
        if self.report_stress_mode == "assert":
            raise errors.PhysicsError(msg)
        elif self.report_stress_mode == "warn":
            warnings.warn(msg)
        elif self.report_stress_mode == "write":
            tqdm.write(msg)

    def clean_cache(self):
        if self.DEBUG:
            print("Clearing cache")
        shutil.rmtree(
            os.path.join("fem", "fenics", "cache", ".cache"), ignore_errors=True
        )
        shutil.rmtree(
            os.path.join("fem", "fenics", "cache", ".ccache"), ignore_errors=True
        )
        shutil.rmtree(
            os.path.join("/", "home", "developer", ".cache"), ignore_errors=True
        )

    def _generate_mesh(self, geometry, grid_shape, interpolation_order=1, cutout=None):
        num_grid_dims = len(geometry)
        vert_grid_shape = np.asarray(
            np.ceil(np.divide(grid_shape, interpolation_order)), dtype=np.int32
        )

        # Create mesh
        if num_grid_dims == 2:
            mesh = fx.RectangleMesh(
                fx.Point(0.0, 0.0),
                fx.Point(geometry[0], geometry[1]),
                *(vert_grid_shape - 1),
                diagonal="left"
            )
        elif num_grid_dims == 3:
            mesh = fx.BoxMesh(
                fx.Point(0.0, 0.0, 0.0),
                fx.Point(geometry[0], geometry[1], geometry[2]),
                *(vert_grid_shape - 1)
            )
        else:
            raise NotImplementedError("Only 2D and 3D supported!")
        # Optionally cut out rectangle
        if cutout is not None:
            if not hasattr(cutout, "keys"):
                cutout = {"rect0": cutout}
            # Get cells and vertices
            cells = np.asarray(mesh.cells())
            verts = np.asarray(mesh.coordinates())
            # Create new mesh
            new_mesh = fx.Mesh()
            editor = fx.MeshEditor()
            editor.open(
                new_mesh, mesh.cell_name(), mesh.topology().dim(), mesh.geometry().dim()
            )
            # Find vertices outside of cutout rectangle and mask cells outside
            new_cells = np.copy(np.asarray(cells, dtype=np.int64))
            # Loop over all cutouts
            for cutout_name, cutout_area in cutout.items():
                if "rect" not in cutout_name:
                    warnings.warn(
                        Warning("Unknown cutout: {:s}. Skipping...".format(cutout_name))
                    )
                    continue
                new_verts = []
                iv = 0
                for v in verts:
                    if np.any(v <= cutout_area[0, :]) or np.any(v >= cutout_area[1, :]):
                        # Outside: add vertex
                        new_verts.append(v)
                        iv += 1
                    else:
                        # Inside: delete cells, adjust labels and forget vertex
                        new_cells[np.any(new_cells == iv, axis=1), :] = -1
                        new_cells[new_cells > iv] -= 1
                # Filter out potentially overlapping cells (barycentric coords)
                new_verts = np.asarray(new_verts)
                for ic, c in enumerate(new_cells):
                    if np.any(c >= 0):
                        px = new_verts[c, :]
                        A = 0.5 * (
                            -px[1, 1] * px[2, 0]
                            + px[0, 1] * (-px[1, 0] + px[2, 0])
                            + px[0, 0] * (px[1, 1] - px[2, 1])
                            + px[1, 0] * px[2, 1]
                        )
                        cutout_coords = np.asarray(
                            [
                                [cutout_area[0, 0], cutout_area[0, 1]],
                                [cutout_area[1, 0], cutout_area[0, 1]],
                                [cutout_area[1, 0], cutout_area[1, 1]],
                                [cutout_area[0, 0], cutout_area[1, 1]],
                            ]
                        )
                        for cx in cutout_coords:
                            s = (
                                1.0
                                / (2.0 * A)
                                * (
                                    px[0, 1] * px[2, 0]
                                    - px[0, 0] * px[2, 1]
                                    + (px[2, 1] - px[0, 1]) * cx[0]
                                    + (px[0, 0] - px[2, 0]) * cx[1]
                                )
                            )
                            t = (
                                1.0
                                / (2.0 * A)
                                * (
                                    px[0, 0] * px[1, 1]
                                    - px[0, 1] * px[1, 0]
                                    + (px[0, 1] - px[1, 1]) * cx[0]
                                    + (px[1, 0] - px[0, 0]) * cx[1]
                                )
                            )
                            if s > 0.0 and t > 0.0 and 1.0 - s - t > 0.0:
                                new_cells[ic, :] = -1
                                break
                verts = new_verts
                new_cells = new_cells[np.all(new_cells >= 0, axis=1), :]
            # Add vertices and cells to new mesh
            editor.init_vertices(len(new_verts))
            editor.init_cells(len(new_cells))
            for iv, v in enumerate(new_verts):
                editor.add_vertex(iv, v)
            for ic, c in enumerate(new_cells):
                editor.add_cell(ic, c)
            editor.close()
            mesh = new_mesh
            # fig = plt.figure(figsize=(4.0, 3.0))
            # fx.plot(mesh)
            # plt.scatter(cutout_coords[:, 0], cutout_coords[:, 1])
            # plt.savefig('cutout_tmp')
            # plt.close()
        # Store connectivity and vertices
        assert mesh.geometry().dim() == num_grid_dims
        if self.connectivity is None:
            self.connectivity = np.copy(np.asarray(mesh.cells(), dtype=np.int64))
        if self.vertices is None:
            self.vertices = np.copy(np.asarray(mesh.coordinates(), dtype=np.float64))
        if self.bc_fun_kwargs["coords"] is None:
            coords = generate_grid(geometry, grid_shape)
            lower_boundaries = [coords[:, i] == 0.0 for i in range(num_grid_dims)]
            upper_boundaries = [
                coords[:, i] == geometry[i] for i in range(num_grid_dims)
            ]
            mask = np.any(
                np.concatenate([lower_boundaries, upper_boundaries], axis=0), axis=0
            )
            boundary_coords = coords[mask, :]
            self.bc_fun_kwargs["coords"] = boundary_coords
        return mesh

    def _define_boundary_domains(self, geometry):
        num_grid_dims = len(geometry)
        domains = dict()
        cpp_string = "near(x[dim], val) && on_boundary"
        domains["xn"] = fx.CompiledSubDomain(cpp_string, dim=0, val=0.0)
        domains["xp"] = fx.CompiledSubDomain(cpp_string, dim=0, val=geometry[0])
        domains["yn"] = fx.CompiledSubDomain(cpp_string, dim=1, val=0.0)
        domains["yp"] = fx.CompiledSubDomain(cpp_string, dim=1, val=geometry[1])
        if num_grid_dims > 2:
            domains["zn"] = fx.CompiledSubDomain(cpp_string, dim=2, val=0.0)
            domains["zp"] = fx.CompiledSubDomain(cpp_string, dim=2, val=geometry[2])
        domains["all"] = fx.CompiledSubDomain("on_boundary")
        # Pointwise boundary conditions are created individual for each point
        pointwise_cpp = " && ".join(
            ["near(x[{:d}], bcx{:d})".format(d, d) for d in range(num_grid_dims)]
        )
        return domains, pointwise_cpp

    def _assemble_dirichlet_bc(
        self,
        geometry,
        Vu,
        bc_u,
        bc_value_std,
        bc_noise_std=0.0,
        remove_rigid_body_motion=True,
    ):

        num_grid_dims = len(geometry)

        # Define boundaries
        domains, pointwise_cpp = self._define_boundary_domains(geometry)
        coords = self.bc_fun_kwargs["coords"]
        bc_u = self.convert_to_pointwise_boundary_conditions(
            bc_u, bc_value_std, self.bc_fun_kwargs, domains=domains, tol=self.tol
        )

        # Remove rigid body motion
        if remove_rigid_body_motion and self.transform_to_corotational:
            self.urb, self.Rrb = self.extract_rigid_body_motion(
                coords, bc_u["pointwise"]
            )
            bc_u["pointwise"] = self.remove_rigid_body_motion(
                coords, bc_u["pointwise"], self.urb, self.Rrb, rotate_displacements=True
            )

        # Check constrained directions
        self.constrained = np.any(bc_u["pointwise"] != None, axis=0)
        # bc_is_not_global = ((bc_u.get('all') is None
        #                      or np.size(bc_u.get('all')) == 0)
        #                     and (bc_u.get('pointwise') is None
        #                          or np.size(bc_u.get('pointwise')) == 0))
        # if bc_is_not_global:
        #     constrained = [False] * num_grid_dims
        # else:
        #     constrained = [True] * num_grid_dims

        bcs = []
        for bc_name, bc_matrix in bc_u.items():
            if num_grid_dims < 3 and "z" in bc_name:
                continue
            if np.size(bc_matrix) > 0:
                # Read bc fun keyword arguments
                max_val = self.bc_fun_kwargs["max_val"]
                unit_disp = self.bc_fun_kwargs["unit_disp"]
                coords = self.bc_fun_kwargs["coords"]
                if np.ndim(bc_matrix) == 1:
                    # Ensure bc_matrix is at least 2D
                    bc_matrix = np.reshape(bc_matrix, [1, -1])
                    coords = np.reshape(coords, [1, -1])
                # # Ensure same shape for bc values and nodes
                # assert np.shape(bc_matrix) == np.shape(coords)
                # assert np.ndim(bc_matrix) == 2
                # Calculate noise value
                if bc_noise_std and bc_name == "pointwise" and self.bc_noise is None:
                    self.bc_noise = normal(1.0, bc_noise_std, np.shape(coords))
                # Loop over rows in bc_matrix: if only one row, then apply
                #     boundary conditions to all nodes
                for node_id, bcu in enumerate(bc_matrix):
                    for i, v in enumerate(bcu):
                        # Select domain
                        if bc_name != "pointwise":
                            method = "topological"
                            bc_domain = domains[bc_name]
                        else:
                            # Pointwise boundary conditions are applied per node
                            method = "pointwise"
                            # Extract boundary coordinate value
                            bcx = coords[node_id, :]
                            # Create subdomain
                            if num_grid_dims == 2:
                                bc_domain = fx.CompiledSubDomain(
                                    pointwise_cpp, bcx0=bcx[0], bcx1=bcx[1]
                                )
                            elif num_grid_dims == 3:
                                bc_domain = fx.CompiledSubDomain(
                                    pointwise_cpp, bcx0=bcx[0], bcx1=bcx[1], bcx2=bcx[2]
                                )
                            else:
                                raise NotImplementedError
                        # Set value as float or result of function call
                        if v is not None:
                            if callable(v):
                                raise NotImplementedError
                                assert hasattr(v, "cpp_code")
                                cpp_code = copy.deepcopy(v.cpp_code)
                                # Generate random value
                                bc_value = normal(0.0, bc_value_std)
                                # # Add noise to cpp code function
                                # if bc_noise_std:
                                #     # Box Muller transform to generate normal
                                #     #   distributed random number
                                #     box_muller = (
                                #         'sqrt(-2.0 * log2(rand()) / log2(exp(1))) * cos(2.0 * DOLFIN_PI * rand())')
                                #     cpp_code = (
                                #         '(' + cpp_code + ') + bc_noise_std * '
                                #         + box_muller)
                                if num_grid_dims == 2:
                                    c = fx.Expression(
                                        cpp_code,
                                        max_val=max_val,
                                        geometry0=geometry[0],
                                        geometry1=geometry[1],
                                        bc_value=bc_value,
                                        bc_noise_std=bc_noise_std,
                                        unit_disp=unit_disp,
                                        bcx0=bcx[0],
                                        bcx1=bcx[1],
                                        degree=self.interpolation_order,
                                    )
                                elif num_grid_dims == 3:
                                    # add check for z direction to craig bampton
                                    if "near(x[1], bcx1)" in cpp_code:
                                        cpp_code = cpp_code.replace(
                                            "near(x[1], bcx1)",
                                            "near(x[1], bcx1) " "&& near(x[2], bcx2)",
                                        )
                                    c = fx.Expression(
                                        cpp_code,
                                        max_val=max_val,
                                        geometry0=geometry[0],
                                        geometry1=geometry[1],
                                        geometry2=geometry[2],
                                        bc_value=bc_value,
                                        bc_noise_std=bc_noise_std,
                                        unit_disp=unit_disp,
                                        bcx0=bcx[0],
                                        bcx1=bcx[1],
                                        bcx2=bcx[2],
                                        degree=self.interpolation_order,
                                    )
                                else:
                                    raise NotImplementedError
                            else:
                                if self.bc_noise is not None:
                                    c0 = v * self.bc_noise[node_id, i]
                                else:
                                    c0 = v
                                c = fx.Constant(c0)
                            # Set and collect boundary conditions
                            bc = fx.DirichletBC(Vu.sub(i), c, bc_domain, method=method)
                            bc.name = bc_name + (str(i))
                            bcs.append(bc)
                            # constrained[i] = True
        return bcs, self.constrained

    def _assemble_neumann_bc(
        self, geometry, grid_shape, mesh, bc_f, bc_value_std, bc_noise_std=0.0
    ):

        num_grid_dims = len(geometry)

        # Define boundaries
        domains, pointwise_cpp = self._define_boundary_domains(geometry)

        # TODO: convert to pointwise BC?

        # Define and mark boundaries in alphabetical order
        boundaries = fx.MeshFunction("size_t", mesh, mesh.topology().dim() - 1)
        boundaries.set_all(0)
        for i, dk in enumerate(sorted(domains.keys())):
            domains[dk].mark(boundaries, i + 1)
        ds = fx.Measure("ds", domain=mesh, subdomain_data=boundaries)

        # Set boundary conditions
        ti_dsi = []
        for bc_name, bc_matrix in bc_f.items():
            if num_grid_dims < 3 and "z" in bc_name:
                continue
            if np.size(bc_matrix) > 0:
                # Read bc fun keyword arguments
                max_val = self.bc_fun_kwargs["max_val"]
                coords = self.bc_fun_kwargs["coords"]
                if np.ndim(bc_matrix) == 1:
                    # Ensure bc_matrix is at least 2D
                    bc_matrix = np.reshape(bc_matrix, [1, -1])
                    coords = np.reshape(coords, [1, -1])
                # Ensure same shape for bc values and nodes
                assert np.ndim(bc_matrix) == 2
                # Loop over rows in bc_matrix: if only one row, then apply
                #     boundary conditions to all nodes
                for node_id, bcf in enumerate(bc_matrix):
                    ti = []
                    for i, v in enumerate(bcf):
                        # Extract boundary coordinate value
                        bcx = coords[node_id, :]
                        # Select domain
                        if bc_name != "pointwise":
                            bc_domain_id = sorted(domains.keys()).index(bc_name)
                        else:
                            raise NotImplementedError
                            # # Pointwise boundary conditions are individual
                            # method = 'pointwise'
                            # if num_grid_dims == 2:
                            #     bc_domain = fx.CompiledSubDomain(
                            #         pointwise_cpp,
                            #         bcx0=bcx[0], bcx1=bcx[1])
                            # elif num_grid_dims == 3:
                            #     bc_domain = fx.CompiledSubDomain(
                            #         pointwise_cpp,
                            #         bcx0=bcx[0], bcx1=bcx[1], bcx2=bcx[2])
                            # else:
                            #     raise NotImplementedError
                        # Calculate noise value
                        if bc_noise_std:
                            bc_noise = normal(0.0, bc_noise_std)
                        else:
                            bc_noise = 0.0
                        # Set value as float or result of function call
                        if v is not None:
                            if callable(v):
                                assert hasattr(v, "cpp_code")
                                cpp_code = copy.deepcopy(v.cpp_code)
                                # Generate random value
                                bc_value = normal(0.0, bc_value_std)
                                # # Add noise to cpp code function
                                # if bc_noise_std:
                                #     # Box Muller transform to generate normal
                                #     #   distributed random number
                                #     box_muller = (
                                #         'sqrt(-2.0 * log2(rand()) / log2(exp(1))) * cos(2.0 * DOLFIN_PI * rand())')
                                #     cpp_code = (
                                #         '(' + cpp_code + ') + bc_noise_std * '
                                #         + box_muller)
                                if num_grid_dims == 2:
                                    c = fx.Expression(
                                        cpp_code,
                                        max_val=max_val,
                                        geometry0=geometry[0],
                                        geometry1=geometry[1],
                                        bc_value=bc_value,
                                        bc_noise_std=bc_noise_std,
                                        bcx0=bcx[0],
                                        bcx1=bcx[1],
                                        degree=self.interpolation_order,
                                    )
                                elif num_grid_dims == 3:
                                    c = fx.Expression(
                                        cpp_code,
                                        max_val=max_val,
                                        geometry0=geometry[0],
                                        geometry1=geometry[1],
                                        geometry2=geometry[2],
                                        bc_value=bc_value,
                                        bc_noise_std=bc_noise_std,
                                        bcx0=bcx[0],
                                        bcx1=bcx[1],
                                        bcx2=bcx[2],
                                        degree=self.interpolation_order,
                                    )
                                else:
                                    raise NotImplementedError
                            else:
                                c0 = v  # + bc_noise  # add noise
                                c = fx.Constant(c0)
                            # # Scale nodal loads to traction per boundary area
                            # TODO:  Why isn't this necessary anymore?
                            # if bc_name[0] in 'xyz'[:num_grid_dims]:
                            #     normal_dir = 'xyz'[:num_grid_dims].index(
                            #         bc_name[0])
                            #     active_dims = list(range(num_grid_dims))
                            #     del active_dims[normal_dir]
                            #     # Multiply by number of nodes in tangent dir
                            #     load_scale = np.prod(np.asarray(
                            #         grid_shape, np.float64)[active_dims])
                            #     # Divide by boundary area
                            #     load_scale /= np.prod(np.asarray(
                            #         geometry, np.float64)[active_dims])
                            #     # TODO: divide by thickness too?
                            # else:
                            #     load_scale = 1.0
                            load_scale = 1.0
                            # Set and collect boundary conditions
                            ti.append(c * fx.Constant(load_scale))
                        else:
                            ti.append(fx.Constant(0.0))
                    ti_dsi.append((fx.as_vector(tuple(ti)), ds(bc_domain_id + 1)))
        return ti_dsi

    def _gather_results(
        self,
        num_grid_dims,
        xe,
        ue,
        fe,
        se,
        pe=None,
        num_stress_dims=None,
        add_rigid_body_motion=True,
    ):
        num_stress_dims = num_stress_dims or num_grid_dims
        fe_results = dict()
        # Coordinates
        fe_results["Xi"] = xe.reshape([-1, num_grid_dims], order="C")
        # Deformations
        U = np.copy(ue.reshape([-1, num_grid_dims], order="C"))
        fe_results["Ui"] = U
        # Stresses
        if num_stress_dims == 2:
            # Initial ordering: S11, S12, S12, S22
            # Ordering: S11, S22, S12
            stress_component_order = [0, 3, 1]
        elif num_stress_dims == 3:
            # Initial ordering: S11, S12, S13, S12, S22, S23, S13, S23, S33
            # Ordering: S11, S22, S33, S12, S23, S13
            stress_component_order = [0, 4, 8, 1, 5, 2]
        else:
            raise NotImplementedError
        fe_results["Si"] = se.reshape(
            [-1, num_stress_dims * num_stress_dims], order="C"
        )[:, stress_component_order]
        fe_results["Fi"] = fe.reshape([-1, num_grid_dims], order="C")
        # Remove unconstrained rigid body motion due to missing constraints
        if np.any(~self.constrained):
            if self.DEBUG:
                print("Unconstrained directions null-spaced.")
            urb1 = np.mean(fe_results["Ui"], axis=0)
            fe_results["Ui"][:, ~self.constrained] -= urb1[~self.constrained]
        # Add rigid body motion
        if add_rigid_body_motion and self.transform_from_corotational:
            fe_results["Ui"] = self.add_rigid_body_motion(
                fe_results["Xi"],
                fe_results["Ui"],
                self.urb,
                self.Rrb,
                rotate_displacements=True,
            )
            fe_results["Fi"] = self.rotate_forces(fe_results["Fi"], self.Rrb)
            fe_results["Si"] = self.rotate_stresses(fe_results["Si"], self.Rrb)
        if pe is not None:
            fe_results["Pi"] = np.copy(pe)
        return fe_results

    @staticmethod
    def linearized_strain(u):
        eps = fx.sym(fx.nabla_grad(u))
        return eps

    @staticmethod
    def linearized_stress(eps, lb, mu, I):
        return lb * fx.tr(eps) * I + 2.0 * mu * eps

    @staticmethod
    def _2D_to_3D_tensor(T2):
        return fx.as_tensor(
            [[T2[0, 0], T2[0, 1], 0.0], [T2[1, 0], T2[1, 1], 0.0], [0.0, 0.0, 0.0]]
        )

    @staticmethod
    def tensor2voigt(T, dims=None):
        if dims is None:
            dims = T.ufl_shape[0]
        if dims == 2:
            v = fx.as_vector([T[0, 0], T[1, 1], T[0, 1]])
        elif dims == 3:
            v = fx.as_vector([T[0, 0], T[1, 1], T[2, 2], T[0, 1], T[1, 2], T[2, 0]])
        else:
            raise ValueError("dims must be 2 or 3")
        return v

    @staticmethod
    def voigt2tensor(v, dims=None):
        if dims is None:
            dims = v.ufl_shape[0]
        if dims == 2:
            T = fx.as_tensor([[v[0], v[2]], [v[2], v[1]]])
        elif dims == 3:
            T = fx.as_tensor(
                [[v[0], v[3], v[5]], [v[3], v[1], v[4]], [v[5], v[4], v[2]]]
            )
        else:
            raise ValueError("dims must be 2 or 3")
        return T

    @staticmethod
    def local_project_to_numpy_array(v, V, dx=None, shape=None):
        vector = np.asarray(FenicsInterface.local_project(v, V, dx=dx).vector())
        if shape:
            return np.reshape(vector, shape, order="C")
        else:
            return vector

    @staticmethod
    def assign_to_fenics_function(ndarray, V):
        vector = np.ravel(ndarray, order="C")
        var = fx.Function(V)
        FenicsInterface.local_assign(var, vector)
        return var

    @staticmethod
    def local_project(v, V, dx=None, u=None):
        if dx is None:
            dx = fx.dx
        dv = fx.TrialFunction(V)
        v_ = fx.TestFunction(V)
        a_proj = fx.inner(dv, v_) * dx
        b_proj = fx.inner(v, v_) * dx
        solver = fx.LocalSolver(a_proj, b_proj)
        solver.factorize()
        if u is None:
            u = fx.Function(V)
            solver.solve_local_rhs(u)
        else:
            solver.solve_local_rhs(u)
        # if u is None:
        #     u = fx.Function(V)
        # uu = fx.project(v, V)
        # u.assign(uu)
        return u

    @staticmethod
    def local_assign(var, val):
        if isinstance(val, np.ndarray):
            var.vector().set_local(val)
        else:
            var.vector().set_local(val.vector())
        return var

    def _create_pretty_progress_bar(self, postfix):
        if self.VERBOSITY >= 2:
            tqdm_target = sys.stdout
        else:
            tqdm_target = open(os.devnull, "w")
        bar_format = (
            Fore.BLUE + "{l_bar}{bar}| [{elapsed}<{remaining}, "
            "{rate_fmt}{postfix}]" + Style.RESET_ALL
        )
        postfix["iter"] = -1
        postfix["(rel) residual"] = -1.0
        postfix["(rel) displacement"] = -1.0
        postfix["(rel) energy"] = -1.0
        pbar = tqdm(
            total=1.0,
            file=tqdm_target,
            leave=True,
            desc=self.INDENT + "Fenics Newton-Raphson",
            dynamic_ncols=True,
            unit="iter",
            postfix=postfix,
            bar_format=bar_format,
        )
        pbar.target = tqdm_target
        return pbar

    def _update_pretty_progress_bar(
        self, pbar, iter, rel_res, rel_disp, rel_energy, postfix
    ):
        if self.VERBOSITY >= 2:
            postfix["iter"] = iter
            postfix["(rel) residual"] = rel_res
            postfix["(rel) displacement"] = rel_disp
            postfix["(rel) energy"] = rel_energy
            min_rel = np.min([rel_res, rel_disp, rel_energy])
            delta_tol = min(
                0.0,
                ((np.log10(min_rel) - np.log10(self.tol)) / np.log10(self.tol)),
            )
            pbar_val = 1.0 + delta_tol
            pbar.update(max(0.0, pbar_val - pbar.n))

    def linearelastic_cube(
        self,
        geometry,
        material,
        properties,
        grid_shape,
        bc_u,
        fe_state=None,
        bc_f=None,
        bc_value_std=0.0,
        bc_noise_std=0.0,
        cutout=None,
    ):
        """Calculate small displacements of a linear elastic rectangle/cube."""

        ####################################
        # Mesh
        #
        if self.DEBUG:
            print("Generating mesh")

        num_grid_dims = len(geometry)

        mesh = self._generate_mesh(
            geometry,
            grid_shape,
            interpolation_order=self.interpolation_order,
            cutout=cutout,
        )

        # Define function spaces
        Vu = fx.VectorFunctionSpace(mesh, "CG", self.interpolation_order)
        Vs = fx.TensorFunctionSpace(mesh, "CG", self.interpolation_order)
        dVs = fx.TensorFunctionSpace(mesh, "DG", self.interpolation_order - 1)

        ####################################
        # Boundary conditions
        #
        if self.DEBUG:
            print("Generating boundary conditions")

        bcs, constrained = self._assemble_dirichlet_bc(
            geometry,
            Vu,
            bc_u,
            bc_value_std,
            bc_noise_std=bc_noise_std,
            remove_rigid_body_motion=True,
        )
        if bc_f is not None:
            ti_dsi = self._assemble_neumann_bc(
                geometry,
                grid_shape,
                mesh,
                bc_f,
                bc_value_std,
                bc_noise_std=bc_noise_std,
            )
        else:
            ti_dsi = []

        ####################################
        # Partial differential equation
        #
        if self.DEBUG:
            print("Defining PDE")

        # Define functions
        du = fx.TrialFunction(Vu)  # trial displacement
        u_ = fx.TestFunction(Vu)  # test displacement
        u = fx.Function(Vu)  # displacement
        b0 = fx.Constant(
            tuple([0.0] * num_grid_dims)
        )  # TODO: Body force per unit volume

        # Kinematics
        dims = len(u)
        n = fx.FacetNormal(mesh)  # Normal vector
        I = fx.Identity(dims)  # Identity tensor
        if dims == 2:
            d = fx.Constant(properties[0])
        else:
            d = fx.Constant(1.0)

        # Define engineering strain
        eps = self.linearized_strain(u)

        # Elasticity parameters
        E0 = fx.Constant(material[0])
        nu = fx.Constant(material[1])
        mu = E0 / (2.0 * (1.0 + nu))
        lb = E0 * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
        if dims == 2 and self.plane_stress:
            lb = 2.0 * mu * lb / (lb + 2.0 * mu)

        # Define engineering stress
        sig = self.linearized_stress(eps, lb, mu, I)

        Pi_inner = 0.5 * d * fx.inner(sig, eps) * fx.dx
        Pi_outer = fx.inner(b0, u) * d * fx.dx
        if bc_f is not None:
            for ti, dsi in ti_dsi:
                Pi_outer += (
                    fx.inner(ti, u) * dsi
                )  # Add traction force (do not multiply with d since ti are calculated from nodal forces
        Pi = Pi_inner - Pi_outer

        # Define loads
        r = fx.derivative(Pi, u, u_)
        f = fx.derivative(Pi_inner, u, u_)

        # Define tangent stiffness
        K = fx.derivative(f, u, du)
        Kt = fx.derivative(r, u, du)

        ###################################
        # Solve variational problem
        #
        if self.DEBUG:
            print("Solving variational problem")

        solver_params = dict()
        # solver_params['newton_solver'] = dict()
        # solver_params['newton_solver']['absolute_tolerance'] = 1e-10   # 1e-10
        # solver_params['newton_solver']['relative_tolerance'] = 1e-9   # 1e-9
        # solver_params['newton_solver']['maximum_iterations'] = 50     # 50
        # solver_params['newton_solver']['relaxation_parameter'] = 1.0
        # solver_params['linear_solver'] = 'lu'
        # solver_params['preconditioner'] = 'ilu'
        # solver_params['krylov_solver'] = dict()
        # solver_params['krylov_solver']['absolute_tolerance'] = 1E-9
        # solver_params['krylov_solver']['relative_tolerance'] = 1E-7
        # solver_params['krylov_solver']['maximum_iterations'] = 1000
        # solver_params['krylov_solver']['gmres']['restart'] = 40
        # solver_params['krylov_solver']['preconditioner']['ilu']['fill_level'] = 0}

        fx.solve(r == 0, u, bcs, J=Kt, solver_parameters=solver_params)

        # Project and interpolate
        stress = fx.project(sig, dVs)
        nodal_stress = fx.Function(Vs)
        nodal_stress.interpolate(stress)

        ####################################
        # Post processing
        #
        if self.DEBUG:
            print("")
            print("Post processing")

        # Extract
        xe = np.copy(Vu.tabulate_dof_coordinates()[::num_grid_dims])
        ue = np.copy(np.asarray(u.vector()))
        se = np.copy(np.asarray(nodal_stress.vector()))
        fe = np.copy(np.asarray(fx.assemble(f)))

        # Gather results
        if not self.plane_stress:
            # Initial ordering: S11, S12, S12, S22
            # New ordering: S11, S12, S13, S12, S22, S23, S13, S23, S33
            se = np.reshape(se, [-1, 4], order="C")
            se = np.concatenate(
                [
                    se[:, :2],
                    np.zeros([se.shape[0], 1]),
                    se[:, 2:4],
                    np.zeros([se.shape[0], 3]),
                    material[1] * (se[:, :1] + se[:, 3:4]),
                ],
                axis=-1,
            )
            fe_results = self._gather_results(
                num_grid_dims,
                xe,
                ue,
                fe,
                se,
                num_stress_dims=3,
                add_rigid_body_motion=True,
            )
        else:
            fe_results = self._gather_results(
                num_grid_dims, xe, ue, fe, se, add_rigid_body_motion=True
            )

        # Plot solution
        if self.plot:
            self.plot_fe_state(fe_results, name="linearelastic", grid_shape=grid_shape)

        # Add boundary conditions to fe_results
        fe_results["bc_u"] = bc_u
        fe_results["bc_f"] = bc_f

        if self.DEBUG:
            print("Done.")

        return fe_results

    def hyperelastic_cube(
        self,
        geometry,
        material,
        properties,
        grid_shape,
        bc_u,
        fe_state=None,
        bc_f=None,
        bc_value_std=0.0,
        bc_noise_std=0.0,
        cutout=None,
    ):
        """Calculate finite displacement of a hyperelastic rectangle/cube."""

        ####################################
        # Mesh
        #
        if self.DEBUG:
            print("Generating mesh")

        num_grid_dims = len(geometry)

        mesh = self._generate_mesh(
            geometry,
            grid_shape,
            interpolation_order=self.interpolation_order,
            cutout=cutout,
        )

        # Define function spaces
        Vu = fx.VectorFunctionSpace(mesh, "CG", self.interpolation_order)
        Vs = fx.TensorFunctionSpace(mesh, "CG", self.interpolation_order)
        dVs = fx.TensorFunctionSpace(mesh, "DG", self.interpolation_order - 1)

        ####################################
        # Boundary conditions
        #
        if self.DEBUG:
            print("Generating boundary conditions")

        bcs, constrained = self._assemble_dirichlet_bc(
            geometry,
            Vu,
            bc_u,
            bc_value_std,
            bc_noise_std=bc_noise_std,
            remove_rigid_body_motion=True,
        )
        if bc_f is not None:
            ti_dsi = self._assemble_neumann_bc(
                geometry,
                grid_shape,
                mesh,
                bc_f,
                bc_value_std,
                bc_noise_std=bc_noise_std,
            )
        else:
            ti_dsi = []

        ####################################
        # Partial differential equation
        #
        if self.DEBUG:
            print("Defining PDE")

        # Define functions
        du = fx.TrialFunction(Vu)  # Incremental displacement
        u_ = fx.TestFunction(Vu)  # Test function
        u = fx.Function(Vu)  # Total displacement
        b0 = fx.Constant([0.0] * num_grid_dims)  # Body force per unit volume   # TODO
        t0 = fx.Constant([0.0] * num_grid_dims)  # Traction force on boundary   # TODO

        # Kinematics
        dims = len(u)
        if dims == 2:
            d = fx.Constant(properties[0])
        else:
            d = fx.Constant(1.0)
        I = fx.Identity(dims)  # Identity tensor
        F = I + fx.nabla_grad(u)  # Deformation gradient
        F = fx.variable(F)  # Turn into variable before further use !!!

        # Define strain
        C = F.T * F  # Right Cauchy-Green Strain
        E = 0.5 * (C - I)  # Euler-Lagrange Strain
        b = F * F.T  # Left Cauchy-Green Strain
        e = 0.5 * (I - fx.inv(b))  # Euler-Almansi Strain

        # Invariants of deformation tensors
        Ic = fx.tr(C)
        J = fx.det(F)

        # Elasticity parameters
        E0 = fx.Constant(material[0])
        nu = fx.Constant(material[1])
        mu = E0 / (2 * (1 + nu))
        lb = E0 * nu / ((1 + nu) * (1 - 2 * nu))
        if dims == 2 and self.plane_stress:
            # TODO: This was taken from linear elasticity and must be corrected
            #    This is more work than expected, since one cannot use
            #    incompressibility in this example to calculate a new lb
            lb = 2.0 * mu * lb / (lb + 2.0 * mu)

        # Stored strain energy density (compressible neo-Hookean model)
        psi = mu / 2 * (Ic - 3) - mu * fx.ln(J) + lb / 2 * fx.ln(J) ** 2

        # Total potential energy
        W_inner = psi * d * fx.dx
        W_outer = fx.inner(b0, u) * d * fx.dx + fx.inner(t0, u) * d * fx.ds
        if bc_f is not None:
            for ti, dsi in ti_dsi:
                W_outer += (
                    fx.inner(ti, u) * dsi
                )  # Add traction force (do not multiply with d since ti are calculated from nodal forces
        W = W_inner - W_outer

        # Define loads
        r = fx.derivative(W, u, u_)
        f = fx.derivative(W_inner, u, u_)

        # Define tangent stiffness
        Kt = fx.derivative(r, u, du)

        # Define stress
        P = fx.diff(psi, F)  # Piola-Kirchhoff 1 Stress
        T = fx.inv(J) * P * F.T  # Cauchy True Stress
        Tau = J * T  # Kirchhoff Stress
        S = fx.inv(F) * P  # Piola-Kirchhoff 2 Stress

        ###################################
        # Solve variational problem
        #
        if self.DEBUG:
            print("Solving variational problem")

        solver_params = dict()
        solver_params["newton_solver"] = dict()
        solver_params["newton_solver"]["absolute_tolerance"] = 1e-10  # 1e-10
        solver_params["newton_solver"]["relative_tolerance"] = 1e-9  # 1e-9
        solver_params["newton_solver"]["maximum_iterations"] = 50  # 50
        solver_params["newton_solver"]["relaxation_parameter"] = 1.0
        # solver_params['linear_solver'] = 'gmres'
        # solver_params['preconditioner'] = 'ilu'
        # solver_params['krylov_solver'] = {}
        # solver_params['krylov_solver']['absolute_tolerance'] = 1E-9
        # solver_params['krylov_solver']['relative_tolerance'] = 1E-7
        # solver_params['krylov_solver']['maximum_iterations'] = 1000
        # solver_params['krylov_solver']['gmres']['restart'] = 40
        # solver_params['krylov_solver']['preconditioner']['ilu']['fill_level'] = 0}

        fx.solve(f == 0, u, bcs, J=Kt, solver_parameters=solver_params)

        # Project and interpolate
        stress = fx.project(T, dVs)
        nodal_stress = fx.Function(Vs)
        nodal_stress.interpolate(stress)

        ####################################
        # Post processing
        #
        if self.DEBUG:
            print("")
            print("Post processing")

        # Extract
        xe = np.copy(Vu.tabulate_dof_coordinates()[::num_grid_dims])
        ue = np.copy(np.asarray(u.vector()))
        se = np.copy(np.asarray(nodal_stress.vector()))
        fe = np.copy(np.asarray(fx.assemble(f)))

        # Gather results
        fe_results = self._gather_results(
            num_grid_dims, xe, ue, fe, se, add_rigid_body_motion=True
        )

        # Plot solution
        if self.plot:
            self.plot_fe_state(fe_state, name="hyperelastic", grid_shape=grid_shape)

        # Add boundary conditions to fe_results
        fe_results["bc_u"] = bc_u
        fe_results["bc_f"] = bc_f

        if self.DEBUG:
            print("Done.")

        return fe_results

    def elastoplastic_cube(
        self,
        geometry,
        material,
        properties,
        grid_shape,
        bc_u,
        fe_state=None,
        bc_f=None,
        bc_value_std=0.0,
        bc_noise_std=0.0,
        cutout=None,
    ):

        ####################################
        # Mesh
        #
        if self.DEBUG:
            print("Generating mesh")

        num_grid_dims = len(geometry)

        # Define mesh and function spaces
        mesh = self._generate_mesh(
            geometry,
            grid_shape,
            interpolation_order=self.interpolation_order,
            cutout=cutout,
        )
        Vu = fx.VectorFunctionSpace(mesh, "CG", self.interpolation_order)
        dVs = fx.TensorFunctionSpace(mesh, "DG", self.interpolation_order, (3, 3))
        Vs = fx.TensorFunctionSpace(mesh, "CG", self.interpolation_order, (3, 3))
        dVs0 = fx.FunctionSpace(mesh, "DG", self.interpolation_order)
        Vs0 = fx.FunctionSpace(mesh, "CG", self.interpolation_order)

        ####################################
        # Boundary conditions
        #
        if self.DEBUG:
            print("Generating boundary conditions")

        bcs, constrained = self._assemble_dirichlet_bc(
            geometry,
            Vu,
            bc_u,
            bc_value_std,
            bc_noise_std=bc_noise_std,
            remove_rigid_body_motion=False,
        )
        # only apply boundary condition values at initial increment
        bc_u1 = self.set_boundary_conditions_to_zero(bc_u)
        bcs1, _ = self._assemble_dirichlet_bc(
            geometry,
            Vu,
            bc_u1,
            bc_value_std,
            bc_noise_std=bc_noise_std,
            remove_rigid_body_motion=False,
        )
        if bc_f is not None:
            ti_dsi = self._assemble_neumann_bc(
                geometry,
                grid_shape,
                mesh,
                bc_f,
                bc_value_std,
                bc_noise_std=bc_noise_std,
            )
        else:
            ti_dsi = []

        ####################################
        # Partial differential equation
        #
        if self.DEBUG:
            print("Defining PDE")

        # Define functions
        v = fx.TrialFunction(Vu)  # trial function
        v_ = fx.TestFunction(Vu)  # test function
        u = fx.Function(Vu)  # total displacement
        du = fx.Function(Vu)  # current iteration displacement
        sig = fx.Function(dVs)  # stress
        n_yield = fx.Function(dVs)  # yield surface normal
        p = fx.Function(dVs0)  # cumulative plastic strain
        p_ = fx.Function(dVs0)  # intermediate cumulative plastic strain
        beta = fx.Function(dVs0)  # relative deviatoric stress step

        u_old = fx.Function(Vu)  # previous iteration displacement
        sig_old = fx.Function(dVs)  # previous iteration stress
        n_yield_old = fx.Function(dVs)  # previous iteration yield surface normal
        p_old = fx.Function(dVs0)  # previous iteration cumulative plastic strain
        beta_old = fx.Function(dVs0)  # previous iteration relative deviatoric stress

        # Kinematics
        dims = len(u)
        if dims == 2:
            d = fx.Constant(properties[0])
        else:
            d = fx.Constant(1.0)

        # Elasticity parameters
        E0 = fx.Constant(material[0])
        nu = fx.Constant(material[1])
        mu = E0 / (2.0 * (1.0 + nu))
        lb = E0 * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
        sig0 = material[3]
        Et = fx.Constant(material[4])
        H = E0 * Et / (E0 - Et)

        # Define engineering stress
        def ppos(x):
            return (x + abs(x)) / 2.0

        def stress_update(deps, sig_old, p):
            I3 = fx.Identity(3)  # Identity tensor for stress
            deps = self._2D_to_3D_tensor(deps)
            # Calculate elastic trial stress and mises equivalent stress
            sig_elastic = sig_old + self.linearized_stress(deps, lb, mu, I3)
            s = fx.dev(sig_elastic)
            sig_equivalent = fx.sqrt(3.0 / 2.0 * fx.inner(s, s))
            # Yield criterion
            _sig_elastic = self.local_project_to_numpy_array(
                sig_elastic, dVs, shape=[-1, 9]
            )
            _mu = material[0] / (2.0 * (1.0 + material[1]))
            _s = self.local_project_to_numpy_array(s, dVs, shape=[-1, 9])
            _sig_equivalent = self.local_project_to_numpy_array(
                sig_equivalent, dVs0, shape=[-1, 1]
            )
            _fy = _sig_equivalent - sig0
            _fy_pos = ppos(_fy)
            # Yield surface normal
            _n_yield = self.safe_divide(_s, _sig_equivalent) * _fy_pos / _fy
            # Yield step
            _dp = _fy_pos / (3.0 * _mu)
            _beta = self.safe_divide(3.0 * _mu * _dp, _sig_equivalent)
            _sig = _sig_elastic - _beta * _s
            sig = np.ravel(_sig, order="C")
            n_yield = np.ravel(_n_yield, order="C")
            beta = np.ravel(_beta, order="C")
            dp = np.ravel(_dp, order="C")
            return sig, n_yield, beta, dp

        def stress_tangent(eps, n_yield, beta):
            I = fx.Identity(3)
            N_yield = self._2D_to_3D_tensor(n_yield)
            sig_elastic = self.linearized_stress(eps, lb, mu, I)
            if dims == 2 and self.plane_stress:
                sig_elastic = fx.elem_mult(
                    sig_elastic,
                    fx.as_tensor([[1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]]),
                )
            c1 = 3.0 * mu * (3.0 * mu / (3.0 * mu + H) - beta)
            c2 = 2.0 * mu * beta
            sig_tangent = (
                sig_elastic - c1 * fx.inner(N_yield, eps) * N_yield - c2 * fx.dev(eps)
            )
            if dims == 2 and self.plane_stress:
                sig_tangent = fx.elem_mult(
                    sig_tangent,
                    fx.as_tensor([[1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 0.0]]),
                )
            return sig_tangent

        ####################################
        # Define variational problem
        #

        eps = self._2D_to_3D_tensor(self.linearized_strain(v))  # Linearized strain
        eps_ = self._2D_to_3D_tensor(self.linearized_strain(v_))  # Variational strain
        sig_tangent_ = stress_tangent(eps_, n_yield, beta)  # Tangent variational stress
        a_Newton = fx.inner(sig_tangent_, eps) * d * fx.dx  # Tangent stiffness
        # FIXME: Define the internal force and resisual of the system. Tip: use fx.inner
        #       and fx.dx. Do not forget to multiply with the thikness.
        f_int = None  # Internal force
        res = None  # Internal residual

        if bc_f is not None:
            for ti, dsi in ti_dsi:
                res += fx.inner(ti, v_) * dsi

        ###################################
        # Solve variational problem
        #
        if self.DEBUG:
            print("Solving variational problem")

        # Assemble stiffness matrix and residual vector
        A, Res = fx.assemble_system(a_Newton, res, bcs)
        if self.A0 is None:
            self.A0 = A
            A0 = A
        else:
            A0 = self.A0

        # Create solver
        solver = fx.LUSolver(A, "default")
        solver.parameters["symmetric"] = True

        # Apply old state
        if fe_state:
            if self.DEBUG:
                print("Using old fe_state")
            # Read old state
            if "fenics.u_old" in fe_state.keys():
                self.local_assign(u_old, np.copy(fe_state["fenics.u_old"]))
            if "fenics.sig_old" in fe_state.keys():
                self.local_assign(sig_old, np.copy(fe_state["fenics.sig_old"]))
            if "fenics.n_yield_old" in fe_state.keys():
                self.local_assign(n_yield_old, np.copy(fe_state["fenics.n_yield_old"]))
            if "fenics.beta_old" in fe_state.keys():
                self.local_assign(beta_old, np.copy(fe_state["fenics.beta_old"]))
            if "fenics.p_old" in fe_state.keys():
                self.local_assign(p_old, np.copy(fe_state["fenics.p_old"]))
            # Update current state
            self.local_assign(u, u_old)
            self.local_assign(sig, sig_old)
            self.local_assign(n_yield, n_yield_old)
            self.local_assign(beta, beta_old)
            self.local_assign(p, p_old)

        # Newton-Raphson iterations (with a pretty progress bar)
        iter_states = []
        Res0 = Res
        norm_res0 = Res0.norm("l2")
        if np.isnan(norm_res0):
            raise RuntimeError("NaN in residual")
        if norm_res0 > self.tol ** (-1):
            raise RuntimeError("Initial residual too large!")
        if norm_res0 > self.tol:
            try:
                postfix = OrderedDict()
                with self._create_pretty_progress_bar(postfix) as pbar:
                    for iter in range(self.max_iteration):
                        # FIXME: Calculate displacement increment Du. Du is change from
                        #        the old displacement to the current displacement.
                        #        Tip: use solver.solve to solve the assembled system of
                        #        the stiffness matrix A and resuidual vector Res for
                        #        du.vector(). The solver will update the du vector with
                        #        the solution. Compute the dispacement increment Du
                        #        afterwards.
                        # solver.solve(...)
                        u.assign(u + du)
                        Du = None
                        deps = self.linearized_strain(Du)
                        # Calculate residual
                        sig_, n_yield_, beta_, dp_ = stress_update(deps, sig_old, p)
                        # Update stress variables
                        self.local_assign(sig, sig_)
                        self.local_assign(n_yield, n_yield_)
                        self.local_assign(beta, beta_)
                        # Calculate energy
                        # FIXME: calculate the system energy from the displacement
                        #        increment and the current residual. Tip: use np.dot to
                        #        calculate the inner product of the corresponding
                        #        discrete vectors.
                        energy = None
                        if iter == 0:
                            energy0 = energy
                        # Update stiffness and residual
                        if self.regularization < 1.0:
                            A, Res = fx.assemble_system(a_Newton, res, bcs1)
                            # Regularize stiffness update
                            A = (
                                1.0 - self.regularization
                            ) * A + self.regularization * A0
                        else:
                            Res = fx.assemble(res)
                            for bc1 in bcs1:
                                bc1.apply(Res)
                        # Convergence criteria
                        norm_res = Res.norm("l2")
                        norm_du = du.vector().norm("l2")
                        norm_u = u.vector().norm("l2")
                        rel_res = norm_res / norm_res0
                        rel_disp = norm_du / norm_u
                        rel_energy = energy / energy0
                        postfix = OrderedDict()
                        self._update_pretty_progress_bar(
                            pbar, iter, rel_res, rel_disp, rel_energy, postfix
                        )
                        if rel_energy < self.tol:
                            if self.VERBOSITY >= 2:
                                postfix["converged"] = (
                                    Fore.GREEN + "True:Energy" + Fore.BLUE
                                )
                                pbar.set_postfix(postfix)
                            break
                        elif rel_res < self.tol:
                            if self.VERBOSITY >= 2:
                                postfix["converged"] = (
                                    Fore.GREEN + "True:Residual" + Fore.BLUE
                                )
                                pbar.set_postfix(postfix)
                            break
                        elif rel_disp < self.tol:
                            if self.VERBOSITY >= 2:
                                postfix["converged"] = (
                                    Fore.GREEN + "True:Displacement" + Fore.BLUE
                                )
                                pbar.set_postfix(postfix)
                            break
                        elif iter == self.max_iteration - 1:
                            if self.VERBOSITY >= 2:
                                postfix["converged"] = (
                                    Fore.RED + "False:MaxIter" + Fore.BLUE
                                )
                                pbar.set_postfix(postfix)
                            raise RuntimeError("Maximum number of iterations reached.")
                        else:
                            if self.VERBOSITY >= 2:
                                pbar.set_postfix(postfix)
                            # Extract fe state
                            self.local_assign(p_, np.asarray(p.vector()) + dp_)
                            iter_state = self._elastoplastic_extract_fe_state(
                                Vu, Vs, Vs0, num_grid_dims, u, sig, p_, f_int
                            )
                            # Ensure mises stress does not exceed yield stress
                            if self.report_stress_mode:
                                mises = self.extract_stress_values(iter_state["Si"])
                                tol_factor = 1.0 + 1e7 * self.tol
                                if np.any(mises > tol_factor * material[3]):
                                    msg = (
                                        "Mises stress exceeds yield stress: "
                                        + "{:.14g} > {:.14g} * {:g}".format(
                                            np.max(mises), tol_factor, sig0
                                        )
                                    )
                                    self.report(msg)
                            iter_states.append(iter_state)
            finally:
                if pbar.target is not sys.stdout:
                    pbar.target.close()
            self.local_assign(p, np.asarray(p.vector()) + dp_)

            if self.DEBUG:
                print("max(du):", np.max(np.asarray(du.vector())))
                print("max(u):", np.max(np.asarray(u.vector())))
                print("max(sig):", np.max(np.asarray(sig.vector())))
                print("_______________________________________________________")

        ####################################
        # Post processing
        #
        if self.DEBUG:
            print("")
            print("Post processing")

        # Extract fe state
        fe_results = self._elastoplastic_extract_fe_state(
            Vu, Vs, Vs0, num_grid_dims, u, sig, p, f_int
        )

        # Ensure mises stress does not exceed yield stress
        if self.report_stress_mode:
            mises = self.extract_stress_values(fe_results["Si"])
            tol_factor = 1.1  # (1.0 + 100.0 * self.tol)
            if np.any(mises > tol_factor * material[3]):
                msg = (
                    "Mises stress exceeds yield stress: "
                    + "{:.14g} > {:.14g} * {:g}".format(
                        np.max(mises), tol_factor, material[3]
                    )
                )
                self.report(msg)

        # Add fenics state to fe_results
        fe_results["fenics.u_old"] = np.copy(np.asarray(u.vector()))
        fe_results["fenics.sig_old"] = np.copy(np.asarray(sig.vector()))
        fe_results["fenics.n_yield_old"] = np.copy(np.asarray(n_yield.vector()))
        fe_results["fenics.p_old"] = np.copy(np.asarray(p.vector()))
        fe_results["fenics.beta_old"] = np.copy(np.asarray(beta.vector()))

        # Add iteration states to fe_results
        if iter_states:
            fe_results["iter_states"] = iter_states

        # Add initial state to fe_results
        if self.return_initial_state:
            if fe_state:
                fe_results["Ui0"] = np.copy(fe_state["Ui"])
                fe_results["Si0"] = np.copy(fe_state["Si"])
                fe_results["Fi0"] = np.copy(fe_state["Fi"])
                fe_results["Pi0"] = np.copy(fe_state["Pi"])
            else:
                fe_results["Ui0"] = np.zeros_like(fe_results["Ui"])
                fe_results["Si0"] = np.zeros_like(fe_results["Si"])
                fe_results["Fi0"] = np.zeros_like(fe_results["Fi"])
                fe_results["Pi0"] = np.copy(fe_results["Pi"])

        # Add boundary conditions to fe_results
        fe_results["bc_u"] = bc_u
        fe_results["bc_f"] = bc_f

        if self.DEBUG:
            print("Done.")

        return fe_results

    def _elastoplastic_extract_fe_state(
        self, Vu, Vs, Vs0, num_grid_dims, u, sig, p, f_int
    ):
        # Project and interpolate
        stress = self.local_project(sig, Vs, dx=fx.dx)
        plastic_strain = self.local_project(p, Vs0, dx=fx.dx)
        # stress = self.local_project(
        #     sig, fx.TensorFunctionSpace(
        #         mesh, 'DG', self.interpolation_order - 1, shape=(3, 3)), dx=dxm)
        # stress = fx.project(stress, Vs)
        # plastic_strain = self.local_project(
        #     p, fx.FunctionSpace(
        #         mesh, 'DG', self.interpolation_order - 1), dx=dxm)
        # plastic_strain = fx.project(plastic_strain, Vs0)

        # Extract
        xe = np.copy(Vu.tabulate_dof_coordinates()[::num_grid_dims])
        ue = np.copy(np.asarray(u.vector()))
        se = np.copy(np.asarray(stress.vector()))
        pe = np.copy(np.asarray(plastic_strain.vector()))
        fe = np.copy(np.asarray(fx.assemble(f_int)))

        # Reshape stresses
        se = np.reshape(se, [-1, 9], order="C")
        pe = np.reshape(pe, [-1, 1], order="C")

        # Gather results
        fe_results = self._gather_results(
            num_grid_dims,
            xe,
            ue,
            fe,
            se,
            pe=pe,
            num_stress_dims=3,
            add_rigid_body_motion=False,
        )
        return fe_results

    def _fenics_plot_displacement_stresses(self, u, sig, name):
        fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
        fig.set_tight_layout("True")
        plt.sca(axes[0])
        plt.title("displacements")
        plt.axis("equal")
        pu = fx.plot(u, mode="displacement")
        pu.set_cmap("jet")
        plt.colorbar(pu, rasterized=True)
        plt.sca(axes[1])
        plt.title("von Mises stresses")
        plt.axis("equal")
        s = fx.dev(sig)
        sig_mises = fx.sqrt(3.0 / 2.0 * fx.inner(s, s))
        ps = fx.plot(sig_mises)
        ps.set_cmap("jet")
        plt.colorbar(ps, rasterized=True)
        plt.draw()
        path = os.path.join(
            "RESULTS",
            "test",
            "{:s}_u0={:.3f}.png".format(name, np.max(np.asarray(u.vector()))),
        )
        path = path.replace(".", "_")
        path = path.replace("_png", ".png")
        plt.savefig(path)
        plt.close(fig)
        os.chmod(path, 0o666)
