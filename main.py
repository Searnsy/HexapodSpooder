import pygame
import os
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PhysicsEngine import *
from PhysicsEngine.Objects import *


ground_vertices = (
    (-100,0,-100),
    (-100,0,100),
    (100,0,100),
    (100,0,-100)
    )

display = (1200, 1000)

# Camera settings
render_distance = 1000
camera_speed = 0.1
turn_speed = 0.1

camera = Camera(Vec3D(6.03287383962069, 16.25283763032475, 27.887075411683966), Vec3D(0.028347915216693907, -0.4036161725900322, -1.0000504907469956))
mouse_held = False


def handle_keys():
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        camera.move_forward(camera_speed)
    if keys[K_s]:
        camera.move_forward(-camera_speed)
    if keys[K_a]:
        camera.move_right(-camera_speed)
    if keys[K_d]:
        camera.move_right(camera_speed)
    if keys[K_SPACE]:
        camera.move_up(camera_speed)
    if keys[K_LSHIFT]:
        camera.move_up(-camera_speed)


def handle_mouse():
    global mouse_held
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left mouse button is held down
        if not mouse_held:
            pygame.mouse.get_rel()  # Reset mouse movement to avoid initial jump
            mouse_held = True
        else:
            mouse_rel = pygame.mouse.get_rel()
            theta = math.atan2(mouse_rel[0], mouse_rel[1])
            rel_length = math.sqrt(mouse_rel[0]**2 + mouse_rel[1]**2)
            if rel_length > 1:
                # print('mouse rel: ' + str(mouse_rel) + '; theta: ' + str(theta) + '; rel_length: ' + str(rel_length))
                camera.change_look_angle((theta + math.pi / 2), turn_speed)


def update_camera():
    glLoadIdentity()
    global display
    gluPerspective(45, (display[0] / display[1]), 0.1, render_distance)
    gluLookAt(
        camera.position.x, camera.position.y, camera.position.z,  # Camera position
        camera.position.x + camera.look_direction.x, camera.position.y + camera.look_direction.y, camera.position.z + camera.look_direction.z,  # Look at x
        camera.up_direction.x, camera.up_direction.y, camera.up_direction.z
    )
    # print('camera pos:' + str(camera.position) + '; look_angle: ' + str(camera.look_direction))


def main():
    global display
    pygame.init()

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.RESIZABLE)

    # Set up perspective
    gluPerspective(45, (display[0] / display[1]), 0.1, render_distance)
    glTranslatef(10.0, 0, 10.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    ground = RigidSurface(Vec3D(0.0, 0.0, 0.0), 1.0, Vec3D(0, 1.0, 0), ground_vertices)
    cube = Cube(Vec3D(1.0, 1.0, 1.0), 1, 2)
    sphere = Sphere(Vec3D(3.0, 8.0, 1.0), 1.0, 3, 2)
    sphere2 = Sphere(Vec3D(4.0, 14.0, 1.0), 1.0, 2, 2)

    # cube.add_force(Vec3D(0.0, -1, 0.0), None)
    sphere.add_force(Vec3D(0.0, -1.0, 0.0), None)
    sphere2.add_force(Vec3D(0.0, -1.0, 0.0), None)

    obj = PhysicsObject(Vec3D(0, 2.0, 0), 1.0)
    obj.add_force(Vec3D(0.0, -1, 0.0), None)
    sphere.velocity = Vec3D(1.0, 6.0, 0.0)

    engine = PhysicsEngine()
    engine.add_object(cube)
    engine.add_object(sphere)
    engine.add_object(sphere2)
    engine.add_object(obj)
    engine.add_object(ground)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                print('resizing: ' + str(event))
                display = (event.w, event.h)

        handle_keys()
        handle_mouse()
        update_camera()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for obj in engine.objects:
            obj.draw()
        pygame.display.flip()

        engine.step_time()
        pygame.time.wait(10)
        # pygame.event.wait()


if __name__ == "__main__":
    main()
