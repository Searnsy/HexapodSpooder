from abc import ABC, abstractmethod
from ..Vec3D import Vec3D


class PhysicsObject:
    def __init__(self, position, mass):
        self.position = position    # The position of the center of mass
        self.velocity = Vec3D(0.0, 0.0, 0.0)
        self.mass = mass
        self.forces = []

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def check_collision(self, obj2) -> None:
        pass

    def step_time(self, time_delta):
        translation_acceleration = Vec3D(0.0, 0.0, 0.0)
        # rotation_acceleration = Vec3D(0.0, 0.0, 0.0)
        for (force, source_point) in self.forces:
            if source_point is not None:
                translation_direction = self.position - source_point
                translation_force = translation_direction.proj(force)
                # rotation_force = force - translation_force

                translation_acceleration += translation_force / self.mass
                # rotation_acceleration += rotation_force / (self.mass * translation_direction.norm())
            else:
                translation_acceleration += force / self.mass

        self.position += self.velocity * time_delta + 0.5 * translation_acceleration * time_delta**2
        self.velocity += translation_acceleration * time_delta

        # TODO: account for rotational forces still here

    def add_force(self, force, source_point):
        self.forces.append((force, source_point))
