from OpenGL.GL import *
from .PhysicsObject import PhysicsObject
from ..Vec3D import Vec3D


class Cube(PhysicsObject):
    def __init__(self, position, mass, side_length):
        # Define vertices, edges, surfaces, and colors of a cube
        super().__init__(position, mass)
        self.side_length = side_length
        self.vertices = [
            (position.x - side_length/2, position.y - side_length/2, position.z - side_length/2),
            (position.x + side_length/2, position.y - side_length/2, position.z - side_length/2),
            (position.x + side_length/2, position.y + side_length/2, position.z - side_length/2),
            (position.x - side_length/2, position.y + side_length/2, position.z - side_length/2),
            (position.x - side_length/2, position.y - side_length/2, position.z + side_length/2),
            (position.x + side_length/2, position.y - side_length/2, position.z + side_length/2),
            (position.x + side_length/2, position.y + side_length/2, position.z + side_length/2),
            (position.x - side_length/2, position.y + side_length/2, position.z + side_length/2),
        ]

        self.edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7)
        )

        self.surfaces = (
            (0, 3, 2, 1),
            (3, 7, 6, 2),
            (5, 6, 7, 4),
            (5, 4, 0, 1),
            (1, 2, 6, 5),
            (0, 4, 7, 3)
        )

        self.colors = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 1, 0),
            (1, 0, 1),
            (0, 1, 1)
        ]

    def update_coords(self):
        side_length = self.side_length
        position = self.position
        self.vertices = [
            (position.x - side_length / 2, position.y - side_length / 2, position.z - side_length / 2),
            (position.x + side_length / 2, position.y - side_length / 2, position.z - side_length / 2),
            (position.x + side_length / 2, position.y + side_length / 2, position.z - side_length / 2),
            (position.x - side_length / 2, position.y + side_length / 2, position.z - side_length / 2),
            (position.x - side_length / 2, position.y - side_length / 2, position.z + side_length / 2),
            (position.x + side_length / 2, position.y - side_length / 2, position.z + side_length / 2),
            (position.x + side_length / 2, position.y + side_length / 2, position.z + side_length / 2),
            (position.x - side_length / 2, position.y + side_length / 2, position.z + side_length / 2),
        ]
        if position.y - side_length/2 <= 0.0 and len(self.forces) == 1:
            self.add_force(Vec3D(0, 50, 0), None)
        elif len(self.forces) > 1:
            self.forces.pop(-1)

    def check_collision(self, obj2) -> None:
        pass

    def draw(self):
        self.update_coords()
        glBegin(GL_QUADS)
        for i, surface in enumerate(self.surfaces):
            glColor3fv(self.colors[i])
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()