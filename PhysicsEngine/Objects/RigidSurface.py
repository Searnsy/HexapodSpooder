from OpenGL.GL import *
from ..Vec3D import Vec3D
from .PhysicsObject import PhysicsObject


class RigidSurface(PhysicsObject):
    def __init__(self, position, mass, normal, vertices, color=(0.9, 0.9, 0.9)):
        super().__init__(position, mass)
        self.normal = normal

        self.vertices = vertices

        self.color = color

    def step_time(self, time_delta):
        pass

    def check_collision(self, obj2) -> None:
        pass

    def draw(self):
        glBegin(GL_QUADS)
        glColor3fv(self.color)
        for vertex in self.vertices:
            glVertex3fv(vertex)
        glEnd()