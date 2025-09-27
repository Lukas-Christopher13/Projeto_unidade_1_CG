import numpy as np

from tkinter import *
from OpenGL.GL import *

def cartesiam_plane():
    points = np.array([
        [-1.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 1.0],
        [0.0, -1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],

    ], dtype=np.float32)

    glColor3f(1,0,0)
    glBegin(GL_LINES)
    for p in points:
        glVertex4fv(p)
    glEnd()
    
