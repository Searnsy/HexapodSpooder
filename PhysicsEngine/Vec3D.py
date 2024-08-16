from math import sqrt
import numbers


class Vec3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vec3D(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vec3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3D):
            return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
        elif isinstance(other, numbers.Number):
            return Vec3D(self.x * other, self.y * other, self.z * other)
        raise NotImplementedError

    def __rmul__(self, other):
        return Vec3D(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vec3D(self.x / other, self.y / other, self.z / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def dot(self, other):
        return self * other

    def cross(self, other):
        return Vec3D(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def norm(self):
        return sqrt(self * self)

    def proj_length(self, other):
        return self.dot(other) / (self.dot(self))

    def proj(self, other):
        return self.proj_length(other) * self

    def normalize(self):
        norm = self.norm()
        return Vec3D(self.x/norm, self.y/norm, self.z/norm)

    def to_array(self):
        return (self.x, self.y, self.z)


def main():
    x = Vec3D(1, 2, 3)
    y = Vec3D(4, 5, 6)
    print('x: ' + str(x) + '; y: ' + str(y))
    print('x + y: ' + str(x + y))
    print('x - y: ' + str(x - y))
    print('x * y: ' + str(x * y))
    print('x.dot(y): ' + str(x.dot(y)))
    print('x.cross(y): ' + str(x.cross(y)))
    print('x.norm(): ' + str(x.norm()))
    print('x.proj_length(y): ' + str(x.proj_length(y)))
    print('x.proj(y): ' + str(x.proj(y)))


if __name__ == '__main__':
    main()
