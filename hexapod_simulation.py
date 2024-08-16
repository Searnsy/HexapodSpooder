import numpy as np
from PhysicsEngine.Objects import PhysicsObject


class Leg:
    def __init__(self, starting_hip_angle=0.0, starting_knee_angle=0.0):
        """
        Initializes the leg with appropriate angles at the hip and knee

        :param starting_hip_angle: the angle of the upper leg in the x-y plane,
            measured in degrees ccw from the x-axis
        :param starting_knee_angle: the angle of the lower leg in the leg-z plane,
            measured in degrees outward from the negative z-axis
        """
        self.upper_leg_length = 5
        self.lower_leg_length = 5
        self.upper_leg_mass = 0.25
        self.lower_leg_mass = 0.25
        self.total_mass = self.upper_leg_mass + self.lower_leg_mass
        self.angles = (starting_hip_angle, starting_knee_angle)
        self.starting_angles = self.angles
        self.knee_position = self.compute_knee_position(self.angles)
        self.foot_position = self.compute_foot_position(self.angles)

    def compute_knee_position(self, angles):
        """
        Computes the knee position as an offset vector from the body of the hexapod.

        :param angles: the (hip, knee) angle of the leg
        :return: the position of the knee in (x, y, z) space
        """
        hip_angle, knee_angle = angles
        x = self.upper_leg_length * np.cos(hip_angle)
        y = self.upper_leg_length * np.sin(hip_angle)
        z = 0.0
        return np.array([x, y, z])

    def compute_foot_position(self, angles):
        """
        Computes the foot position as an offset vector from the body of the hexapod.

        :param angles: the (hip, knee) angle of the leg
        :return: the position of the foot in (x, y, z) space
        """
        hip_angle, knee_angle = angles
        x, y, z = self.compute_knee_position(angles)
        x += self.lower_leg_length * np.cos(hip_angle) * np.sin(knee_angle)
        y += self.lower_leg_length * np.sin(hip_angle) * np.sin(knee_angle)
        z += -self.lower_leg_length * np.cos(knee_angle)
        return np.array([x, y, z])

    def compute_relative_center_of_mass(self):
        upper_center_of_mass = self.knee_position / 2
        lower_center_of_mass = (self.foot_position + self.knee_position) / 2
        return (self.upper_leg_mass * upper_center_of_mass + self.lower_leg_mass * lower_center_of_mass) / self.total_mass

    def reset(self):
        self.angles = self.starting_angles
        self.knee_position = self.compute_knee_position(self.angles)
        self.foot_position = self.compute_foot_position(self.angles)

    def draw(self, body_position, body_rotation):
        pass


class HexapodSimulation(PhysicsObject):
    def __init__(self, position, mass):
        super().__init__(position, mass)
        default_leg_hip_angles = [60, 90, 120, -60, -90, -120]
        self.legs = [Leg(starting_hip_angle=angle) for angle in default_leg_hip_angles]
        self.starting_body_position = position
        self.starting_body_rotation = np.array([0.0, 0.0, 0.0, 0.0]) # Quaternion rotation (?)

        self.body_position = self.starting_body_position
        self.body_position_prev = self.starting_body_position
        self.body_rotation = self.starting_body_rotation
        self.body_rotation_prev = self.starting_body_position
        self.body_velocity = np.array([0.0, 0.0, 0.0])
        self.body_mass = mass

    def check_collision(self, obj2) -> None:
        pass

    def draw(self) -> None:
        for leg in self.legs:
            # Compute the leg's coordinates relative to the global coordinate system
            leg.draw(self.body_position, self.body_rotation)


    def step_simulation(self, time_step=0.1):
        forces = []
        forces.append(np.array([0.0, 0.0, -9.8])) # Gravity
        total_force = np.sum(forces)
        self.body_velocity += total_force * time_step / self.body_mass
        self.body_position += self.body_velocity

    def compute_center_of_mass(self):
        center_of_mass = self.body_position * self.body_mass
        total_mass = self.body_mass
        for leg in self.legs:
            # TODO: use quaternion rotations to put the leg into the relative coordinates of the body
            center_of_mass += self.get_relative_position(leg.compute_relative_center_of_mass()) * leg.total_mass
            total_mass += leg.total_mass
        center_of_mass /= total_mass

    def apply_torques(self, torques_per_leg):
        for leg_index in range(6):
            hip_torque, knee_torque = torques_per_leg[leg_index]
            # if self.legs[leg_index].foot_position[2] > 0.0:
                # Foot is in the air, so we can rotate it without applying a force on the body
            # else:
                # Foot is in contact with the ground, so we can rotate it

    def reset(self):
        self.body_position = self.starting_body_position
        self.body_position_prev = self.starting_body_position
        self.body_velocity = np.array([0.0, 0.0, 0.0])
        for leg in self.legs:
            leg.reset()

