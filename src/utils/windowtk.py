import numpy as np

from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *


class WindowTk(OpenGLFrame):
    gl_option = GL_POINTS
    main_vertex = vertices = np.empty((0, 4), dtype=np.float32)

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._render = lambda: None
        self._init_config = lambda: None

    def initgl(self):
        glClearColor(1, 1, 1, 1)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(1, 0, 0)
        glBegin(self.gl_option)
        for v in self.main_vertex:
            glVertex4fv(v)
        glEnd()

        glFlush()

    def update(self, gl_option, np_array):
        self.gl_option = gl_option
        self.main_vertex = np.vstack([self.main_vertex, np_array])

    def clear(self):
        self.main_vertex = np.empty((0, 4), dtype=np.float32)
