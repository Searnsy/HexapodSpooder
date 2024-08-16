import pygame.display
from OpenGL.GL import *
from .PhysicsObject import PhysicsObject
from .RigidSurface import RigidSurface
from ..Vec3D import Vec3D
import random


class Sphere(PhysicsObject):
    def __init__(self, position, mass, radius, subdivisions):
        # Define vertices, edges, surfaces, and colors of a cube
        super().__init__(position, mass)
        self.radius = radius
        self.points = []
        self.points_base = []
        self.edges = []
        self.triangles = self.compute_subdivisions(subdivisions)
        self.simplify_triangles()
        self.color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

    def subdivide_triangle(self, triangle, subdivisions):
        if subdivisions == 0:
            return [triangle]
        A = triangle[0]
        B = triangle[1]
        C = triangle[2]
        D, E, F = (A + B) / 2, (B + C) / 2, (A + C) / 2
        D, E, F = D.normalize() * self.radius, E.normalize() * self.radius, F.normalize() * self.radius
        initial_triangles = [[A, D, F], [D, B, E], [E, C, F], [D, E, F]]
        triangles = []
        for triangle in initial_triangles:
            triangles.extend(self.subdivide_triangle(triangle, subdivisions - 1))
        return triangles

    def compute_subdivisions(self, subdivisions):
        initial_triangles = [
            [Vec3D(self.radius, 0, 0), Vec3D(0, self.radius, 0), Vec3D(0, 0, self.radius)],
            [Vec3D(0, 0, -self.radius), Vec3D(0, self.radius, 0), Vec3D(self.radius, 0, 0)],
            [Vec3D(-self.radius, 0, 0), Vec3D(0, self.radius, 0), Vec3D(0, 0, -self.radius)],
            [Vec3D(0, 0, self.radius), Vec3D(0, self.radius, 0), Vec3D(-self.radius, 0, 0)],
            [Vec3D(0, 0, self.radius), Vec3D(0, -self.radius, 0), Vec3D(self.radius, 0, 0)],
            [Vec3D(self.radius, 0, 0), Vec3D(0, -self.radius, 0), Vec3D(0, 0, -self.radius)],
            [Vec3D(0, 0, -self.radius), Vec3D(0, -self.radius, 0), Vec3D(-self.radius, 0, 0)],
            [Vec3D(-self.radius, 0, 0), Vec3D(0, -self.radius, 0), Vec3D(0, 0, self.radius)]]
        triangles = []
        for triangle in initial_triangles:
            triangles.extend(self.subdivide_triangle(triangle, subdivisions))
        return triangles

    def simplify_triangles(self):
        points = []
        triangle_indices = []
        edge_indices = []
        for triangle in self.triangles:
            tri = []
            for vertex in triangle:
                if vertex not in points:
                    points.append(vertex)
                tri.append(points.index(vertex))
            triangle_indices.append(tri)
            if ([points.index(triangle[0]), points.index(triangle[1])]) not in edge_indices:
                edge_indices.append([points.index(triangle[0]), points.index(triangle[1])])
            if ([points.index(triangle[1]), points.index(triangle[2])]) not in edge_indices:
                edge_indices.append([points.index(triangle[1]), points.index(triangle[2])])
            if ([points.index(triangle[2]), points.index(triangle[0])]) not in edge_indices:
                edge_indices.append([points.index(triangle[2]), points.index(triangle[0])])
        self.points = points
        self.points_base = points
        self.triangles = triangle_indices
        self.edges = edge_indices

    def update_coords(self):
        self.points = [point + self.position for point in self.points_base]

        # if self.position.y - self.radius <= 0.0 and len(self.forces) == 1:
        #     self.add_force(Vec3D(0, 50, 0), None)
        # elif len(self.forces) > 1:
        #     self.forces.pop(-1)

    def check_collision(self, obj2) -> None:
        if isinstance(obj2, RigidSurface):
            dist = (obj2.normal.proj(self.position - obj2.position)).norm()
            if dist <= self.radius:
                velocity_proj = obj2.normal.proj(self.velocity)
                self.velocity = (-velocity_proj + (self.velocity - velocity_proj)) * 0.9 # elasticity should be a constant
        elif isinstance(obj2, Sphere):
            if (self.position - obj2.position).norm() <= (self.radius + obj2.radius):
                e = 1.0
                # The two spheres are colliding - apply conservation of momentum to them
                collision_direction = self.position - obj2.position
                self_velocity_proj = collision_direction.proj(self.velocity)
                other_velocity_proj = collision_direction.proj(obj2.velocity)
                self_velocity_tang = self.velocity - self_velocity_proj
                other_velocity_tang = obj2.velocity - other_velocity_proj

                total_mass = self.mass + obj2.mass
                self.velocity = ((self.mass - e * obj2.mass) / total_mass) * self_velocity_proj + (((1+e) * obj2.mass)/total_mass) * other_velocity_proj + self_velocity_tang
                obj2.velocity = ((obj2.mass - e * self.mass) / total_mass) * other_velocity_proj + (((1+e) * self.mass)/total_mass) * self_velocity_proj + other_velocity_tang

                # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                # ground_vertices = (
                #     (-100, 0, -100),
                #     (-100, 0, 100),
                #     (100, 0, 100),
                #     (100, 0, -100)
                # )
                # glBegin(GL_QUADS)
                #
                # for vertex in ground_vertices:
                #     glColor3fv((0.9, 0.9, 0.9))
                #     glVertex3fv(vertex)
                # glEnd()
                # self.draw()
                # obj2.draw()
                # glBegin(GL_LINES)
                #
                # glColor3f(0, 1, 0)
                # glVertex(self.position.to_array())
                # glVertex((self.position - collision_direction).to_array())
                #
                # glColor3f(0, 1, 1)
                # glVertex(self.position.to_array())
                # glVertex((self.position + self_bounce_direction).to_array())
                #
                # glColor3f(0, 1, 1)
                # glVertex(obj2.position.to_array())
                # glVertex((obj2.position + other_bounce_direction).to_array())
                #
                # glEnd()
                # pygame.display.flip()
                # print('hello')

    def draw(self):
        self.update_coords()
        glBegin(GL_TRIANGLES)
        glColor3fv(self.color)
        for triangle in self.triangles:
            for vertex in triangle:
                glVertex3fv(self.points[vertex].to_array())
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.points[vertex].to_array())
        glColor3f(1, 0, 0)

        # Draw the velocity vector
        # glVertex(self.position.to_array())
        # glVertex((self.position + self.velocity).to_array())
        glEnd()