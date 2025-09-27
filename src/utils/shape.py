import numpy as np

from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *


class Shape():
    #set_id
    gl_option = GL_TRIANGLE_FAN
    gl_color = np.empty([0, 0, 1], dtype=np.float32)

    def __init__(self, matrix):
        self.vertex = np.array(matrix, dtype=np.float32)
    
    def render(self):
        glColor3f(0,0,1)
        glBegin(self.gl_option)
        for v in self.vertex:
            glVertex4fv(v)
        glEnd()
    
    def update(self, gl_option, np_array):
        self.gl_option = gl_option
        self.vertex = np.vstack([self.vertex, np_array])

    def clear(self):
        self.vertex = np.empty((0, 4), dtype=np.float32)

    
