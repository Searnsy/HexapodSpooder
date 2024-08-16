import numpy as np
from .Vec3D import Vec3D


class Camera:
    def __init__(self, position, look_direction):
        self.position = position
        self.look_direction = look_direction.normalize()
        self.up_direction = Vec3D(0.0, 1.0, 0.0)

    def sort_points_by_distance(self, points):
        """
        Sorts a list of points based on their distance from the camera in the direction of look angle
        :param points: the points to sort
        :return: a list of indices corresponding to the sorted distances in ascending distance (note some may be negative)
        """
        relative_points = [(point - self.position) for point in points]
        relative_projection = [self.projection_length(self.look_direction, relative_point) for relative_point in relative_points]
        return np.argsort(relative_projection)

    def projection_length(self, a, b):
        """
        Computes the length of the projection of b onto a

        :param a: a vector
        :param b: a vector
        :return: the projection of b onto a
        """
        return np.dot(a, b) / (np.norm(a) * np.norm(b))

    def move_forward(self, step_size):
        self.position += self.look_direction * step_size

    def move_right(self, step_size):
        right_direction = self.look_direction.cross(self.up_direction).normalize()
        self.position += right_direction * step_size

    def move_up(self, step_size):
        self.position.y += step_size

    def change_look_angle(self, theta, step_size):
        right_direction = self.look_direction.cross(self.up_direction).normalize()
        angle_change = (np.cos(theta) * right_direction + np.sin(theta) * self.up_direction).normalize()
        self.look_direction += angle_change * step_size
