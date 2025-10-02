import numpy as np

from math import cos, sin, radians

from tkinter import *
from OpenGL.GL import *

class Shape():
    gl_color = np.empty([0, 0, 1], dtype=np.float32)

    def __init__(self, matrix, gl_option):
        self.vertex = np.array(matrix, dtype=np.float32)
        self.gl_option = gl_option
    
    def render(self):
        glColor3f(0,0,1)
        glBegin(self.gl_option)
        for v in self.vertex:
            glVertex4fv(v)
        glEnd()
    
    def update(self, gl_option, np_array):
        self.gl_option = gl_option
        self.vertex = np.vstack([self.vertex, np_array])

    def transform(self, tranformations: list):
        for i in tranformations:
            self.vertex = self.vertex @ i.T
        return self.vertex

    def clear(self):
        self.vertex = np.empty((0, 4), dtype=np.float32)

    def mid_point_vertex(self):
        x_mean, y_mean, z_mean, w_mean = self.vertex.mean(axis=0)
        return [x_mean, y_mean, z_mean, w_mean]
            





    
