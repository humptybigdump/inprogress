import warnings
import numpy as np


class Physics(object):

    @staticmethod
    def extract_stress_values(stresses, stress_type="mises"):
        """Calculate scalar stress values along the last axis of stresses."""
        if stress_type == "mises":
            if stresses.shape[-1] == 6:
                sig_xx = stresses[..., 0]
                sig_yy = stresses[..., 1]
                sig_zz = stresses[..., 2]
                tau_xy = stresses[..., 3]
                tau_yz = stresses[..., 4]
                tau_zx = stresses[..., 5]
            elif stresses.shape[-1] == 3:
                # Plane stress case
                sig_xx = stresses[..., 0]
                sig_yy = stresses[..., 1]
                sig_zz = 0.0
                tau_xy = stresses[..., 2]
                tau_yz = 0.0
                tau_zx = 0.0
            else:
                raise NotImplementedError
            sig_scalar = np.sqrt(
                0.5
                * (
                    (sig_xx - sig_yy) ** 2
                    + (sig_yy - sig_zz) ** 2
                    + (sig_zz - sig_xx) ** 2
                    + 6 * (tau_xy**2 + tau_yz**2 + tau_zx**2)
                )
            )
        elif isinstance(stress_type, int):
            sig_scalar = stresses[..., stress_type]
        else:
            raise ValueError("Invalid stress type: {:s}".format(str(stress_type)))
        return sig_scalar

    @staticmethod
    def extract_rigid_body_motion(xi, ui):
        mask = ui == None
        # Rigid body translation
        urb = np.mean(ui, axis=0)
        # Rigid body rotation
        mu_xi = np.mean(xi, axis=0)
        xc = xi - mu_xi
        xc_ui = np.copy(xc)
        xc_ui[~mask] += np.asarray(ui[~mask], dtype=np.float64)
        xc_ui -= urb
        A_ui = np.cross(xc, xc_ui, axis=-1)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            mask = np.abs(A_ui) > 10.0 * np.finfo("float64").eps  # mask zeros
        if np.any(mask):
            A_ui = A_ui[mask]
            phi = np.arcsin(
                A_ui
                / np.linalg.norm(xc[mask, :], axis=1)
                / np.linalg.norm(xc_ui[mask, :], axis=1)
            )
            n = A_ui / np.linalg.norm(A_ui)
            phirb = np.mean(phi, axis=0)
            nrb = np.mean(n, axis=0)
            Rrb = np.asarray(
                [[np.cos(phirb), -np.sin(phirb)], [np.sin(phirb), np.cos(phirb)]]
            )
        else:
            Rrb = np.identity(xc.shape[-1])
        return urb, Rrb

    @staticmethod
    def remove_rigid_body_motion(
        xi, ui, urb, Rrb, rotate_displacements=True, rotate_translation=False
    ):
        """Add rigid body translation and rotation to fe results."""
        un = np.copy(ui)
        un = np.ma.array(un, dtype=np.float64, mask=(un == None))
        # Remove rigid body translation
        if rotate_translation:
            un -= Physics.rotate_displacements(urb, Rrb)
        else:
            un -= urb
        # Remove rigid body rotation
        mu_xi = np.mean(xi, axis=0)
        xc = xi - mu_xi
        un -= np.dot(xc, Rrb.T) - xc
        # Rotate displacements to new orientation
        if rotate_displacements:
            un = np.ma.array(
                Physics.rotate_displacements(un.filled(0.0), Rrb.T), mask=un.mask
            )
        # Replace Nans with nones
        mask = un.mask
        if np.any(mask):
            un = np.asarray(un, dtype=object)
            un[mask] = None
        else:
            un = np.asarray(un, dtype=np.float64)
        return un

    @staticmethod
    def add_rigid_body_motion(
        xi, un, urb, Rrb, rotate_displacements=True, rotate_translation=False
    ):
        """Add rigid body translation and rotation to fe results."""
        ui = np.copy(un)
        ui = np.asarray(ui, dtype=np.float64)  # Turn None into NaN
        # Rotate displacements to new orientation
        if rotate_displacements:
            ui = Physics.rotate_displacements(ui, Rrb)
        # Add rigid body translation
        if rotate_translation:
            ui += Physics.rotate_displacements(urb, Rrb)
        else:
            ui += urb
        # Add rigid body rotation
        mu_xi = np.mean(xi, axis=0)
        xc = xi - mu_xi
        ui += np.dot(xc, Rrb.T) - xc
        # Replace Nans with nones
        mask = np.isnan(ui)
        if np.any(mask):
            ui = np.asarray(ui, dtype=object)
            ui[mask] = None
        else:
            ui = np.asarray(ui, dtype=np.float64)
        return ui

    @staticmethod
    def rotate_displacements(ui, R):
        return np.dot(ui, R.T)

    @staticmethod
    def rotate_forces(fi, R):
        return np.dot(fi, R.T)

    @staticmethod
    def rotate_stresses(si, R):
        if R.shape[-1] == 3:
            raise NotImplementedError("Rotation in 3D not implemented!")
        if si.shape[-1] == 3:
            # Ordering: S11, S22, S12
            i12 = 2
        elif si.shape[-1] == 6:
            # Ordering: S11, S22, S33, S12, S23, S13
            i12 = 3
        R = np.identity(si.shape[-1])
        R[0, 0] = R[0, 0] ** 2
        R[1, 0] = R[1, 0] ** 2
        R[2, 0] = -R[1, 0] * R[0, 0]
        R[0, 1] = R[0, 1] ** 2
        R[1, 1] = R[1, 1] ** 2
        R[2, 1] = -R[0, 1] * R[1, 1]
        R[0, 2] = -2.0 * R[0, 1] * R[0, 0]
        R[1, 2] = -2.0 * R[1, 0] * R[0, 0]
        R[2, 2] = R[1, 1] ** 2 - R[0, 1] ** 2
        return np.dot(si, R.T)

    @staticmethod
    def safe_divide(a, b, tol=None):
        if tol is None:
            tol = 10.0 * max(np.finfo(a.dtype).eps, np.finfo(b.dtype).eps)
        return np.divide(a, b, out=np.zeros_like(a), where=np.abs(b) > tol)
