import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PhysicsEngine.Camera import Camera
from PhysicsEngine.Vec3D import Vec3D

# Define vertices, edges, surfaces, and colors of a cube
vertices = [
    (0, 0, 0),
    (2, 0, 0),
    (2, 2, 0),
    (0, 2, 0),
    (0, 0, 2),
    (2, 0, 2),
    (2, 2, 2),
    (0, 2, 2),
]

edges = (
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

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 6, 7),
    (5, 4, 7, 6),
    (5, 1, 0, 4),
    (1, 5, 6, 2),
    (0, 3, 7, 4)
)

colors = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1)
]

ground_surfaces = (0,1,2,3)

ground_vertices = (
    (-100,0,-100),
    (100,0,-100),
    (100,0,100),
    (-100,0,100)
    )

# Camera settings
camera_pos = [0.0, 1.0, 5.0]  # Initial position of the camera
camera_speed = 0.1
turn_speed = 0.1

camera = Camera(Vec3D(0.0, 3.0, 5.0), Vec3D(0.0, -0.1, -1.0))
mouse_held = False


def draw_cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0,0,0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_ground():
    glBegin(GL_QUADS)

    for vertex in ground_vertices:
        glColor3fv((0.9, 0.9, 0.9))
        glVertex3fv(vertex)

    # for line in ground_lines:
    #     glColor3fv((0.9, 0.9, 0.9))
    #     glVertex3fv(line)
    glEnd()


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
                print('mouse rel: ' + str(mouse_rel) + '; theta: ' + str(theta) + '; rel_length: ' + str(rel_length))
                camera.change_look_angle((theta + math.pi / 2), turn_speed)


def update_camera():
    glLoadIdentity()
    display = (800, 600)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    gluLookAt(
        camera.position.x, camera.position.y, camera.position.z,  # Camera position
        camera.position.x + camera.look_direction.x, camera.position.y + camera.look_direction.y, camera.position.z + camera.look_direction.z,  # Look at x
        camera.up_direction.x, camera.up_direction.y, camera.up_direction.z
    )


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Set up perspective
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(10.0, 0, 10.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        handle_keys()
        handle_mouse()
        update_camera()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()
        draw_ground()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
