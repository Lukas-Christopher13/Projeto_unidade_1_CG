import numpy as np

from tkinter import *
from OpenGL.GL import *

from src.models.shape import Shape

axies_2d_points = np.array([
    [-10000.0, 0.0,    0.0, 1.0,    0.0, 0.0, 1.0],
    [ 10000.0, 0.0,    0.0, 1.0,    0.0, 0.0, 1.0],
    [ 0.0,   -10000.0, 0.0, 1.0,    1.0, 0.0, 0.0],
    [ 0.0,    10000.0, 0.0, 1.0,    1.0, 0.0, 0.0],
],dtype=np.float32)

axies_3d_points = np.array([
    [0.0, 0.0, 0.0, 1.0,       1.0, 0.0, 0.0],
    [10000.0, 0.0, 0.0, 1.0,    1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1,         0.0, 0.0, 1.0],
    [0.0, 10000.0, 0.0, 1,     0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1,         0.0, 1.0, 0.0],
    [0.0, 0.0, 10000.0, 1,     0.0, 1.0, 0.0]
],dtype=np.float32)

axies_2d = Shape(matrix=axies_2d_points, gl_option=GL_LINES, name="2d axies")
axies_3d = Shape(matrix=axies_3d_points, gl_option=GL_LINES)


