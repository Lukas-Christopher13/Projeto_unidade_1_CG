import numpy as np

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

    def clear(self):
        self.vertex = np.empty((0, 4), dtype=np.float32)

    def translate(self, x: np.float32, y: np.float32, z=0.0):
        translation = np.array([
            [1.0, 0.0, 0.0, x  ],
            [0.0, 1.0, 0.0, y  ],
            [0.0, 0.0, 1.0, z  ],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

        self.vertex = self.vertex @ translation.T


    
