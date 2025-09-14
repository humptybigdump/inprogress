import sys
import copy
import numpy as np
import matplotlib.pyplot as plt
import warnings
import colorama

colorama.init()

from pathlib import Path
from colorama import Fore, Back, Style
from tqdm.autonotebook import tqdm
from collections import OrderedDict
from matplotlib.patches import PathPatch
from ..base import grids
from ..base import errors
from ..base.physics import Physics
from ..base.random import normal
from ..base.history import History


class BaseInterface(Physics):

    VERBOSITY = 1
    INDENT = ""
    DEBUG = False

    def __init__(self, plot=False, write=False):
        """An interface for partial differential equation solvers.

        Args:
            plot:       optional: plot the result in a window
            write:      optional: write the result to a .pvd file
        """
        self.plot = plot
        self.write = write
        self.climits = None
        # Mesh and interpolation
        self.interpolation_order = 2
        self.max_iteration = 100
        self.tol = 1e-9
        self.regularization = 1.0
        self.min_increment = 1
        self.max_increment = 100
        self.inc_down_scale_factor = 0.5
        self.inc_up_scale_factor = 1.5
        self.max_converged = 10
        self.max_iteration = 100
        self.min_delta = 1e-3
        self.max_control = 1.0
        self.rigid_body_constraints = []
        self.count = 0
        # Rigid body motion variables
        self.transform_to_corotational = True
        self.transform_from_corotational = True
        self.urb = np.asarray([0.0, 0.0])
        self.Rrb = np.identity(2)
        self.vertices = None
        self.connectivity = None
        self.bc_fun_args = ()
        self.bc_fun_kwargs = {"max_val": 0.0, "unit_disp": 0.0, "coords": None}
        self.bc_noise = None

    @staticmethod
    def calc_boundary_grid(geometry, grid_shape):
        grid_labels = grids.calc_grid_labels(grid_shape)
        boundary_grid_labels = grids.extract_boundary_grid_labels(
            grid_labels, grid_shape
        )
        grid = grids.generate_grid(geometry, grid_shape)
        return grid[boundary_grid_labels - 1, :]

    def adaptive_time_increments(
        self,
        solve_function,
        geometry,
        material,
        properties,
        grid_shape,
        bc_u,
        fe_state=None,
        bc_f=None,
        bc_value_std=0.1,
        bc_noise_std=0.0,
        cutout=None,
        only_last_state=False,
        ensure_control_values=None,
    ):
        """Adaptive time incrementation for various solve functions."""
        # Store base value of bc_fun_kwargs and bc value/noise std
        base_max_val = copy.copy(self.bc_fun_kwargs["max_val"])
        base_bc_value_std = copy.copy(bc_value_std)
        base_bc_noise_std = copy.copy(bc_noise_std)
        if ensure_control_values is not None:
            ensure_control_values = np.unique(np.asarray(ensure_control_values))
        # Convert to pointwise boundary conditions
        if self.bc_fun_kwargs["coords"] is None:
            grid_labels = grids.calc_grid_labels(grid_shape)
            boundary_grid_labels = grids.extract_boundary_grid_labels(
                grid_labels, grid_shape
            )
            grid = grids.generate_grid(geometry, grid_shape)
            self.bc_fun_kwargs["coords"] = grid[boundary_grid_labels - 1, :]
        coords = self.bc_fun_kwargs["coords"]
        bc_u = self.convert_to_pointwise_boundary_conditions(
            bc_u, bc_value_std, self.bc_fun_kwargs, tol=self.tol
        )
        # # Remove rigid body motion
        # #   This is done in the interface
        # if self.transform_to_corotational:
        #     urb, Rrb = self.extract_rigid_body_motion(
        #         coords, bc_u['pointwise'])
        #     bc_u['pointwise'] = self.remove_rigid_body_motion(
        #         coords, bc_u['pointwise'], urb, Rrb,
        #         rotate_displacements=True)
        # Prepare loop
        fe_history = History()
        old_fe_state = fe_state
        fe_history[0.0] = fe_state
        num_converged = 0
        delta = self.max_control / float(self.min_increment)
        real_delta = delta
        # Overwrite delta to value
        if ensure_control_values is not None:
            check = delta > ensure_control_values
            if np.any(check):
                real_delta = delta
                delta = ensure_control_values[0]
                ensure_control_values = ensure_control_values[1:]
        # Set control value
        control = delta
        # Get old boundary conditions for interpolation
        if fe_history[0.0]:
            bc_u_old = fe_history[0.0]["bc_u"]
            bc_f_old = fe_history[0.0]["bc_f"]
        else:
            bc_u_old = None
            bc_f_old = None

        if self.VERBOSITY:
            tqdm_target = sys.stdout
        else:
            tqdm_target = open(os.devnull, "w")
        bar_format = (
            Fore.BLUE
            + Style.BRIGHT
            + "{l_bar}{bar}| [{elapsed}<{remaining}, "
            + "{rate_fmt}{postfix}]"
            + Style.RESET_ALL
        )
        postfix = OrderedDict()
        postfix["inc"] = -1
        postfix["delta"] = -1.0
        postfix["control"] = -1.0
        try:
            with tqdm(
                total=self.max_control,
                file=tqdm_target,
                leave=True,
                desc=self.INDENT
                + "Interface increments: {:s}".format(solve_function.__name__),
                dynamic_ncols=True,
                unit="inc",
                bar_format=bar_format,
                postfix=postfix,
            ) as pbar:
                if self.VERBOSITY:
                    write = pbar.write
                else:
                    write = print
                for inc in range(self.max_increment):
                    if self.VERBOSITY:
                        postfix = OrderedDict()
                        postfix["inc"] = inc
                        postfix["delta"] = delta
                        postfix["control"] = control
                        pbar.set_postfix(postfix)
                    # Interpolate between old and new boundary conditions using
                    #   the control variable
                    bc_du = self.incremental_boundary_conditions(
                        bc_u, delta, bc_dict_old=bc_u_old
                    )
                    bc_fi = self.scale_boundary_conditions(
                        bc_f, control, bc_dict_old=bc_f_old
                    )
                    # Also scale bc_fun_kwargs and bc value/noise function bcs
                    # TODO: Interpolate between old max_val and new max_val
                    self.bc_fun_kwargs["max_val"] = delta * base_max_val
                    bc_value_std = delta * base_bc_value_std
                    bc_noise_std = delta * base_bc_noise_std
                    try:
                        # Run
                        fe_state = solve_function(
                            geometry,
                            material,
                            properties,
                            grid_shape,
                            bc_du,
                            fe_state=old_fe_state,
                            bc_f=bc_fi,
                            bc_value_std=bc_value_std,
                            bc_noise_std=bc_noise_std,
                            cutout=cutout,
                        )
                        if self.VERBOSITY:
                            pbar.update(max(control - pbar.n, 0.0))
                    except (RuntimeError, errors.PhysicsError) as e:
                        write("    " + e.args[0])
                        if self.VERBOSITY >= 3:
                            write("    " + e.args[0])
                        # Reduce time step size and update step
                        control = max(0.0, control - delta)
                        delta *= self.inc_down_scale_factor
                        control += delta
                        # Set real delta to reduced value too
                        real_delta = delta
                        if self.VERBOSITY >= 3:
                            write(
                                "    Increment diverged. "
                                "Decreasing delta: {:g}".format(delta)
                            )
                        if np.abs(delta) < self.min_delta:
                            if num_converged > 0:
                                if self.VERBOSITY >= 3:
                                    warnings.warn(
                                        "Minimal timestep size reached. "
                                        "Stopping at previous converged step."
                                    )
                                break
                            else:
                                raise RuntimeError("Minimal timestep size reached.")
                    else:
                        # Turn incremental to integral boundary conditions
                        if fe_history[-1]:
                            fe_state["bc_u"] = self.integral_boundary_conditions(
                                fe_history[-1]["bc_u"], bc_du
                            )
                        else:
                            fe_state["bc_u"] = bc_du
                        fe_state["bc_f"] = bc_fi
                        # # Add rigid body motion
                        # #   This is done in the interface
                        # if self.transform_from_corotational:
                        #     fe_state['Ui'] = self.add_rigid_body_motion(
                        #         fe_state['Xi'], fe_state['Ui'], urb, Rrb,
                        #         rotate_displacements=True)
                        #     fe_state['Fi'] = self.rotate_forces(
                        #         fe_state['Fi'], Rrb)
                        #     fe_state['Si'] = self.rotate_stresses(
                        #         fe_state['Si'], Rrb)
                        # Plot solution
                        if self.plot:
                            scale = (
                                0.1
                                * control
                                * np.max(np.abs(fe_state["Xi"]))
                                / np.max(np.abs(fe_state["Ui"]))
                            )
                            self.plot_fe_state(
                                fe_state,
                                name="run{:d}_{:03d}".format(
                                    self.count, int(100 * control)
                                ),
                                grid_shape=grid_shape,
                                draw_nodes=False,
                                displacement_scale=scale,
                            )
                        # Update history
                        fe_history[control] = fe_state
                        # Break condition
                        if control == self.max_control:
                            # The update step rule should ensure that this happens
                            break
                        # Update fe_state
                        old_fe_state = fe_state
                        # Increase time step size if multiple steps converged
                        num_converged += 1
                        if num_converged % self.max_converged == 0:
                            delta *= self.inc_up_scale_factor
                            if self.VERBOSITY >= 3:
                                write(
                                    "    Multiple converged increments. "
                                    "Increasing delta: {:g}".format(delta)
                                )
                        # Overwrite delta value if near ensured control value
                        if ensure_control_values is not None:
                            delta = real_delta  # Reset delta
                            check = (control + delta) > ensure_control_values
                            if np.any(check):
                                real_delta = delta
                                delta = ensure_control_values[0] - control
                                ensure_control_values = ensure_control_values[1:]
                        # Update step
                        if control + delta > self.max_control - self.tol:
                            delta = self.max_control - control
                            control = self.max_control
                        else:
                            control += delta
                        if control > self.max_control + self.tol:
                            raise RuntimeError(
                                "Overshot max control: {:f}".format(control)
                            )
                    finally:
                        # Reset bc_fun_kwargs
                        self.bc_fun_kwargs["max_val"] = base_max_val
        finally:
            self.count += 1
            if tqdm_target is not sys.stdout:
                tqdm_target.close()
        if only_last_state:
            return fe_history[-1]
        else:
            return fe_history

    @staticmethod
    def incremental_boundary_conditions(bc_dict, factor, bc_dict_old=None):
        """Scale a dictionary of boundary conditions by a factor."""
        if not bc_dict:
            scaled_bc_dict = bc_dict
        else:
            scaled_bc_dict = copy.deepcopy(bc_dict)
            for k, v in scaled_bc_dict.items():
                if isinstance(v, np.ndarray):
                    # scale ndarrays using scalar ndarray multiplication
                    #   bc_dict can contain None values for free coordinates
                    #   scale only the values that are not none
                    mask = v != None
                    # Subtract previous state
                    if bc_dict_old:
                        scaled_bc_dict[k][mask] -= bc_dict_old[k][mask]
                    scaled_bc_dict[k][mask] *= factor
                elif v:
                    if bc_dict_old:
                        scaled_bc_dict[k] = [
                            factor * (ui - uo) if isinstance(ui, (float, int)) else ui
                            for ui, uo in zip(v, bc_dict_old[k])
                        ]
                    else:
                        scaled_bc_dict[k] = [
                            factor * ui if isinstance(ui, (float, int)) else ui
                            for ui in v
                        ]
        return scaled_bc_dict

    @staticmethod
    def scale_boundary_conditions(bc_dict, factor, bc_dict_old=None):
        """Scale a dictionary of boundary conditions by a factor."""
        if not bc_dict:
            scaled_bc_dict = bc_dict
        else:
            scaled_bc_dict = copy.deepcopy(bc_dict)
            for k, v in scaled_bc_dict.items():
                if isinstance(v, np.ndarray):
                    # scale ndarrays using scalar ndarray multiplication
                    #   bc_dict can contain None values for free coordinates
                    #   scale only the values that are not none
                    mask = v != None
                    # Subtract previous state
                    if bc_dict_old:
                        scaled_bc_dict[k][mask] += (1.0 - factor) * bc_dict_old[k][mask]
                    scaled_bc_dict[k][mask] *= factor
                elif v:
                    if bc_dict_old:
                        scaled_bc_dict[k] = [
                            (
                                factor * ui + (1.0 - factor) * uo
                                if isinstance(ui, (float, int))
                                else ui
                            )
                            for ui, uo in zip(v, bc_dict_old[k])
                        ]
                    else:
                        scaled_bc_dict[k] = [
                            factor * ui if isinstance(ui, (float, int)) else ui
                            for ui in v
                        ]
        return scaled_bc_dict

    @staticmethod
    def integral_boundary_conditions(bc_dict, dbc_dict):
        """Scale a dictionary of boundary conditions by a factor."""
        if not bc_dict:
            added_bc_dict = bc_dict
        else:
            added_bc_dict = copy.deepcopy(bc_dict)
            for k, v in dbc_dict.items():
                if isinstance(v, np.ndarray):
                    # scale ndarrays using scalar ndarray multiplication
                    #   bc_dict can contain None values for free coordinates
                    #   scale only the values that are not none
                    mask = v != None
                    # Subtract previous state
                    added_bc_dict[k][mask] += v[mask]
                elif v:
                    added_bc_dict[k] = [
                        uo + dui if not (dui is None or callable(dui)) else dui
                        for uo, dui in zip(bc_dict[k], v)
                    ]
        return added_bc_dict

    @staticmethod
    def convert_to_pointwise_boundary_conditions(
        bc_u, bc_value_std, bc_fun_kwargs, domains=None, tol=1e-8
    ):
        """Convert domain-wise boundary conditions to pointwise."""
        bc_u = copy.deepcopy(bc_u)
        coords = bc_fun_kwargs["coords"]
        if "pointwise" in bc_u.keys() and np.size(bc_u["pointwise"]) > 0:
            pointwise_array = bc_u["pointwise"]
        else:
            pointwise_array = np.full(np.shape(coords), fill_value=None)
        for bc_name, bc_matrix in bc_u.items():
            if bc_name != "pointwise" and np.size(bc_matrix) > 0:
                if not (domains and hasattr(domains[bc_name], "inside")):
                    coords_max = np.max(coords, axis=0)
                    coords_min = np.min(coords, axis=0)
                for dim, val in enumerate(bc_matrix):
                    if val is not None:
                        for node_id, coord in enumerate(coords):
                            if domains and hasattr(domains[bc_name], "inside"):
                                is_inside = domains[bc_name].inside(
                                    np.reshape(coord, [-1, 1]), True
                                )
                            else:
                                if bc_name == "xn":
                                    is_inside = np.abs(coords_min[0] - coord[0]) < tol
                                elif bc_name == "xp":
                                    is_inside = np.abs(coords_max[0] - coord[0]) < tol
                                elif bc_name == "yn":
                                    is_inside = np.abs(coords_min[1] - coord[1]) < tol
                                elif bc_name == "yp":
                                    is_inside = np.abs(coords_max[1] - coord[1]) < tol
                                elif bc_name == "zn":
                                    is_inside = np.abs(coords_min[2] - coord[2]) < tol
                                elif bc_name == "zp":
                                    is_inside = np.abs(coords_max[2] - coord[2]) < tol
                                elif bc_name == "all":
                                    is_inside = np.any(
                                        np.abs(coords_min - coord) < tol
                                    ) or np.any(np.abs(coords_max - coord) < tol)
                                else:
                                    raise ValueError("Unknown domain name " + bc_name)
                            if is_inside:
                                if callable(val):
                                    # Find coordinates in that domain
                                    node = np.concatenate([[node_id + 1], coord])
                                    # Generate random value
                                    bc_value = normal(0.0, bc_value_std)
                                    v = val(
                                        node=node, bc_value=bc_value, **bc_fun_kwargs
                                    )
                                else:
                                    v = val
                                if pointwise_array[node_id, dim] is not None:
                                    # Do not add value here, since the
                                    # superposition of boundary conditions
                                    # already added the secondary and
                                    # consistency constraints at the corner
                                    # nodes
                                    pointwise_array[node_id, dim] = v
                                else:
                                    pointwise_array[node_id, dim] = v
        # Remove non global boundary conditions
        return {"pointwise": pointwise_array}

    @staticmethod
    def set_boundary_conditions_to_zero(bc_u):
        bc_u1 = copy.deepcopy(bc_u)
        for bc_name, bc_values in bc_u1.items():
            if isinstance(bc_values, np.ndarray):
                mask = bc_values != None
                bc_u1[bc_name][mask] = 0.0 * bc_values[mask]
            else:
                bc_u1[bc_name] = [v if v is None else 0.0 for v in bc_values]
        return bc_u1

    def plot_fe_state(
        self,
        fe_state,
        displacement_scale=None,
        grid_shape=None,
        name=None,
        linewidth=1.0,
        edgecolor="k",
        colormap="YlGnBu",
        shading="gouraud",
        draw_connectivity=True,
        draw_nodes=True,
    ):
        """Draws the element into the current axes."""
        # Extract data
        Xi = np.copy(fe_state["Xi"])
        Ui = np.copy(fe_state["Ui"])
        Si = np.copy(fe_state["Si"])
        if displacement_scale is None:
            displacement_scale = 0.1 * np.max(np.abs(Xi)) / np.max(np.abs(Ui))
        # Add outer deformation
        Xi_deformed = Xi + displacement_scale * Ui
        # Mises stress
        sig = self.extract_stress_values(Si, stress_type="mises")
        if self.climits is None:
            # Calculate limits
            vmin = min(np.min(sig), 0.0)
            vmax = max(np.max(sig), 0.0)
            if np.abs(vmax - vmin) < 1e-3:
                vmax = 1.0
                vmin = 0.0
        else:
            vmin = self.climits[0]
            vmax = self.climits[1]
        # Extract current coordinates
        tpc = plt.tripcolor(
            Xi_deformed[:, 0],
            Xi_deformed[:, 1],
            sig,
            shading=shading,
            cmap=colormap,
            edgecolor=edgecolor,
            vmax=vmax,
            vmin=vmin,
            rasterized=True,
        )
        # Plot boundary grid
        if grid_shape is not None:
            origin = np.min(Xi, axis=0)
            geometry = tuple(np.max(Xi, axis=0) - np.min(Xi, axis=0))
            grid_coords = grids.generate_grid(geometry, grid_shape) + origin
            # grid_coords = fe_state['Xi']
            X, body, [U] = grids.grid_encode(grid_coords, grid_shape, Xi, [Ui])
            XU = X + displacement_scale * U
            boundary = grids.find_boundary(body)
            mask = np.squeeze(boundary).astype(np.bool)
            idx_boundary_list = grids.sort_grid_boundary_positive_rotation(
                X[mask, :], grid_shape, is_cube=False
            )
            for i, idx_boundary in enumerate(idx_boundary_list):
                deformed_grid_coords = XU[mask, :]
                path_coords = deformed_grid_coords[idx_boundary, :]
                # for txt, (xx, yy) in enumerate(path_coords):
                #     plt.annotate(txt, (xx, yy), fontsize=6)
                path = grids.assemble_path(path_coords)
                axes = plt.gca()
                max_zorder = max([c.zorder for c in axes.get_children()])
                clip_zorder = max_zorder + 1
                if i == 0:
                    # Create transparent patch for clipping
                    patch = PathPatch(
                        path,
                        facecolor="None",
                        edgecolor=edgecolor,
                        linewidth=linewidth,
                        zorder=clip_zorder,
                    )
                    axes.add_patch(patch)
                    tpc.set_clip_path(patch)
                else:
                    # Create white patch for masking
                    patch = PathPatch(
                        path,
                        facecolor="w",
                        edgecolor=edgecolor,
                        linewidth=linewidth,
                        zorder=clip_zorder,
                    )
                    axes.add_patch(patch)
        # Plot internal element grid
        if draw_connectivity:
            if self.vertices is not None and self.connectivity is not None:
                vertices = self.vertices
                connectivity = self.connectivity
                # Vertices are in a different order than the mesh coordinates
                #   (midpoint nodes missing, order defined by function space)
                order = np.concatenate(
                    [
                        np.where(np.all(np.abs(Xi - v) < self.tol, axis=1))[0]
                        for v in vertices
                    ]
                )
                # Add deformations
                vertices_deformed = vertices + displacement_scale * Ui[order, :]
                # Loop over all elements and create patches
                for con in connectivity:
                    path_coords = vertices_deformed[con, :]
                    path = grids.assemble_path(path_coords)
                    axes = plt.gca()
                    max_zorder = max([c.zorder for c in axes.get_children()])
                    connectivity_zorder = max_zorder + 3
                    patch = PathPatch(
                        path,
                        facecolor="None",
                        edgecolor=edgecolor,
                        linewidth=linewidth / 2.0,
                        zorder=connectivity_zorder,
                    )
                    axes.add_patch(patch)
        # Plot nodes
        if draw_nodes:
            axes = plt.gca()
            max_zorder = max([c.zorder for c in axes.get_children()])
            node_zorder = max_zorder + 2
            plt.plot(
                Xi_deformed[:, 0],
                Xi_deformed[:, 1],
                " o",
                color=edgecolor,
                markersize=linewidth * 3.0,
                zorder=node_zorder,
            )
            if self.DEBUG:
                Ubc = fe_state["bc_u"]["pointwise"]
                coords = self.bc_fun_kwargs["coords"]
                mask = np.logical_not(np.any(Ubc == None, axis=1))
                mask1 = np.logical_not(np.all(Ubc == None, axis=1))
                Xbc_deformed = coords[mask, :] + displacement_scale * Ubc[mask, :]
                Ubc1 = np.copy(Ubc)
                Ubc1[Ubc1 == None] = 0.0
                Xbc_deformed1 = coords[mask, :] + displacement_scale * Ubc1[mask1, :]
                plt.plot(
                    Xbc_deformed1[:, 0],
                    Xbc_deformed1[:, 1],
                    " o",
                    color="b",
                    markersize=linewidth * 3.0,
                    zorder=(max_zorder + 2),
                )
                plt.plot(
                    Xbc_deformed[:, 0],
                    Xbc_deformed[:, 1],
                    " o",
                    color="r",
                    markersize=linewidth * 3.0,
                    zorder=(max_zorder + 3),
                )
        plt.axis("equal")
        plt.colorbar()
        plt.tight_layout()
        if name:
            # Save
            path = Path() / "RESULTS" / f"{name}_u0={np.max(np.abs(Ui)):.6f}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(path)
            plt.close("all")
        return tpc
