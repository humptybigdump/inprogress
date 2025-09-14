import math
import numpy as np
from scipy import optimize


class ArmElement:
    def __init__(self, length, angle=0, angle_range=(-3*np.pi/4, 3*np.pi/4)):
        self.length = length
        self.angle = angle
        self.angle_range = np.array(angle_range)

    def get_end_position(self, offset_position, offset_angle=0):
        gamma = offset_angle + self.angle
        return offset_position + np.array([np.cos(gamma), np.sin(gamma)]) * self.length    

    def set_angle(self, angle):
        self.angle = angle

    def set_length(self, length):
        self.length = length


class KinematicChain:
    def __init__(self, arm_elements):
        self.arm_elements = arm_elements

    def __len__(self):
        return len(self.arm_elements)

    def get_angles(self):
        return np.array([ae.angle for ae in self.arm_elements])

    def set_angle(self, joint_id, angle):
        self.arm_elements[joint_id].set_angle(angle)

    def set_angles(self, angles):
        for ae, angle in zip(self.arm_elements, angles):
            ae.set_angle(angle)

    def get_angle_ranges(self):
        return np.array([ae.angle_range for ae in self.arm_elements])

    def ik(self, target_pos):       
        def target_fn(angles):
            self.set_angles(angles)
            
            end_pos = self.get_joint_positions()[-1]
            residual = target_pos - end_pos
            
            return residual.dot(residual) + 7.5*np.sum(angles**2)
                
        res = optimize.minimize(target_fn, self.get_angles(), (), "TNC", 
                       False, bounds=self.get_angle_ranges(),
                       options={'maxiter': 100})
        self.set_angles(float(c) for c in res.x)

    def get_joint_positions(self):
        positions = []
        pos, angle = np.array([0, 0]), 0
        positions.append(pos)
        for ae in self.arm_elements:
            pos = ae.get_end_position(pos, angle)
            angle = math.fmod(angle + ae.angle, 2*np.pi)
            positions.append(pos)
            
        return positions

    def set_lengths(self, lengths):
        for ae, l in zip(self.arm_elements, lengths):
            ae.set_length(l)
