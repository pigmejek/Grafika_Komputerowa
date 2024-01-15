import math
import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

pyramid_vertices = (
    (-2, 0, -4 / 3),
    (2, 0, -4 / 3),
    (0, 0, 8 / 3),
    (0, math.sqrt(57) / 3, 0)
)

edges = (
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 3),
)

surfaces = (
    (0, 1, 2),
    (2, 0, 3),
    (0, 1, 3),
    (1, 2, 3)
)

ground_vertices = (
    (-700, 0, 800),
    (700, 0, 700),
    (-700, 0, -700),
    (700, 0, -700)
)

def ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0.42, 0.27, 0.26))
        glVertex3fv(vertex)
    glEnd()

def sub_tetras(vertices):
    middlepoints = [[(vertices[edge[0]][0] + vertices[edge[1]][0]) / 2,
                     (vertices[edge[0]][1] + vertices[edge[1]][1]) / 2,
                     (vertices[edge[0]][2] + vertices[edge[1]][2]) / 2] for edge in edges]

    return [
        (vertices[0], middlepoints[0], middlepoints[1], middlepoints[2]),
        (vertices[1], middlepoints[0], middlepoints[3], middlepoints[4]),
        (vertices[2], middlepoints[1], middlepoints[3], middlepoints[5]),
        (vertices[3], middlepoints[2], middlepoints[4], middlepoints[5])
    ]

def main_tetra(vertices, check):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((1, 0.7, 0))
            glVertex3fv(vertices[vertex])
    glEnd()

    if check == 1:
        glBegin(GL_TRIANGLES)
        for i_surface, surface in enumerate(surfaces):
            for vertex in surface:
                glColor3f(0.7, 0.13, 0.13)
                glVertex3fv(vertices[vertex])
        glEnd()

def generating_sub_tetras(vertices, depth, texture_visibility):
    if depth == 0:
        main_tetra(vertices, texture_visibility)
        return
    tetrahedrons = sub_tetras(vertices)
    for tetra in tetrahedrons:
        generating_sub_tetras(tetra, depth - 1, texture_visibility)

def main():
    rotation = 1
    rotation_shift = 0
    rotation_speed = 0.4
    texture_visibility = 1

    input_str = input("Wprowadź liczbę poziomów piramidy Sierpińskiego: ")
    levels = int(input_str)

    pygame.init()
    display = (900, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(70, (display[0] / display[1]), 0.1, 50)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, -0.5, -5)

    glLight(GL_LIGHT0, GL_POSITION, (3, 3, 3, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 0.0, 1.0))
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glLight(GL_LIGHT1, GL_POSITION, (0, 0, -1, 1))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (1.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.0, 1.0, 0.0, 1.0))
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # zoom
                if event.button == 4:
                    glTranslatef(0, 0, 1)
                if event.button == 5:
                    glTranslatef(0, 0, -1)

            if event.type == pygame.KEYDOWN:

                # ruch kamery
                if event.key == pygame.K_UP:
                    glTranslatef(0, 0.5, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -0.5, 0)
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5, 0, 0)


                # control textures
                if event.key == pygame.K_t:
                    if texture_visibility == 0:
                        texture_visibility = 1
                    else:
                        texture_visibility = 0

                # obrot
                    if event.key == pygame.K_r:
                        if rotation == 1:
                            rotation = 0
                        else:
                            rotation = 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ground()

        rotation_shift += rotation_speed if rotation == 1 else 0

        glPushMatrix()
        glRotatef(rotation_shift, 0, 1, 0)
        generating_sub_tetras(pyramid_vertices, levels, texture_visibility)
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(20)

main()


