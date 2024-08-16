from math import sqrt
import numpy as np
from .Vec3D import Vec3D


class Quaternion:
    def __init__(self, s, i, j, k):
        self.s = s
        self.i = i
        self.j = j
        self.k = k

    def __add__(self, other):
        return Quaternion(self.s + other.s,
                          self.i + other.i,
                          self.j + other.j,
                          self.k + other.k)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.s * other.s - self.i * other.i - self.j * other.j - self.k * other.k,
                              self.s * other.i + self.i * other.s + self.j * other.k - self.k * other.j,
                              self.s * other.j - self.i * other.k + self.j * other.s + self.k * other.i,
                              self.s * other.k + self.i * other.j - self.j * other.i + self.k * other.s)
        raise NotImplementedError

    def __rmul__(self, other):
        return Quaternion(self.s * other, self.i * other, self.j * other, self.k * other)

    def __truediv__(self, other):
        return Quaternion(self.s / other, self.i / other, self.j / other, self.k / other)

    def __neg__(self):
        return Quaternion(-self.s, -self.i, -self.j, -self.k)

    def norm(self):
        return sqrt(self.s**2 + self.i**2 + self.j**2 + self.k**2)

    def conj(self):
        return Quaternion(self.s, -self.i, -self.j, -self.k)

    def inv(self):
        self.conj() / (self.norm()**2)
        return self.conj() / (self.norm()**2)

    def interpolate(self, other, u):
        cos_theta = self * other
        if cos_theta > 0:
            # self -> other is short distance around sphere
            theta = np.acos(cos_theta)
            interpolation_point = (np.sin((1 - u) * theta)/np.sin(theta) * self) * (np.sin(u * theta)/np.sin(theta) * other)
            return interpolation_point / interpolation_point.norm()
        else:
            # self -> -other is short distance around sphere
            theta = np.acos(self * (-other))
            interpolation_point = (np.sin((1 - u) * theta) / np.sin(theta) * self) * (np.sin(u * theta) / np.sin(theta) * (-other))
            return interpolation_point / interpolation_point.norm()

    def rotate_vector(self, vector):
        vec = Quaternion(0, vector.x, vector.y, vector.z)
        rot = self * vec * self.inv()
        return Vec3D(rot.i, rot.j, rot.k)