import numpy as np

from tkinter import *
from OpenGL.GL import *

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
    
