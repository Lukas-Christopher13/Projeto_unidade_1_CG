import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from math import radians, tan, sin, cos

# Vértices homogêneos (x, y, z, w)
# Aqui z=0 e w=1 — você pode aplicar matriz 4x4 depois
vertices_hom = np.array([
    [-1.0, -1.0, -1.0, 1.0],  
    [1.0, -1.0, -1.0, 1.0], 
    [1.0,  1.0, -1.0, 1.0],
    [-1.0,  1.0, -1.0, 1.0],
    [-1.0, -1.0,  1.0, 1.0], 
    [1.0, -1.0,  1.0, 1.0], 
    [1.0,  1.0,  1.0, 1.0],
    [-1.0,  1.0,  1.0, 1.0],
], dtype=np.float32)

def renderObject():
    scale = 0.0

    rotation = np.array([
        [cos(scale), -sin(scale), 0.0, 0.0],
        [sin(scale),  cos(scale), 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)
 
    translation = np.array([
        [ 1.0, 0.0, 0.0, 1],
        [ 0.0, 1.0, 0.0, 1],
        [ 0.0, 0.0, 1.0, 1],
        [ 0.0, 0.0, 0.0, 1],
    ], dtype=float)

    FOV = 90.0
    tanHalfFOV = tan(radians(FOV / 2.0 ))
    f = 1/tanHalfFOV

    projection = np.array([
        [ f,   0.0, 0.0, 1],
        [ 0.0, f,   0.0, 1],
        [ 0.0, 0.0, f,   1],
        [ 0.0, 0.0, 0.0, 1],
    ], dtype=float)

    return projection @ translation @ rotation


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_QUADS)
    for v in vertices_hom:
        x, y, z, w = v
        glVertex3d(x, y, z)
    glEnd()

    glutSwapBuffers()


def reshape(w, h):
    glViewport(0, 0, w, h)

    # Projeção ortográfica → SEM perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Espaço [-1,1] x [-1,1]
    gluOrtho2D(-1, 1, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Quadrado 2D - Base para 3D")

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()


if __name__ == "__main__":
    main()
