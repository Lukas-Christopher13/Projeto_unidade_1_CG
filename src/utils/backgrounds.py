import numpy as np

from tkinter import *
from OpenGL.GL import *

from src.models.shape import Shape

def cartesiam_plane(width, height):
    x = width
    y = height

    points = np.array([
        [-x, 0.0, 0.0, 1.0],
        [x, 0.0, 0.0, 1.0],
        [0.0, -y, 0.0, 1.0],
        [0.0, y, 0.0, 1.0],

    ], dtype=np.float32)

    glColor3f(1,0,0)
    glBegin(GL_LINES)
    for p in points:
        glVertex4fv(p)
    glEnd()


axies_3d_points = np.array([
    [0.0, 0.0, 0.0, 1.0],
    [1000.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1],
    [0.0, 10000.0, 0.0, 1],
    [0.0, 0.0, 0.0, 1],
    [0.0, 0.0, 10000.0, 1]
],dtype=np.float32)

axies_3d = Shape(matrix=axies_3d_points, gl_option=GL_LINES)


