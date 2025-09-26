import numpy as np

from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *

from .shape import Shape


class WindowTk(OpenGLFrame):
    shapes = []
    current_shape = 0
    gl_option = GL_POINTS
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._render = lambda: None
        self._init_config = lambda: None
        
    def initgl(self):
        glClearColor(1, 1, 1, 1)

    def redraw(self):
        #criar um objeto shape e adiconar a um shape list
        #cada shape object sera rendereizado aqui
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for shape in self.shapes:
            shape.render()

        glFlush()

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
