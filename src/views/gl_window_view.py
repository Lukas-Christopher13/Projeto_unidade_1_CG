from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from utils.backgrounds import cartesiam_plane


class GlWindowView(OpenGLFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        
    def initgl(self):
        glClearColor (1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(-1000, 1000, -1000, 1000) # Passar esse valor
        glMatrixMode (GL_MODELVIEW)

        glClearColor(1, 1, 1, 1)

    def redraw(self):
        width = self.winfo_width()
        height = self.winfo_height()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.resize_window(width, height)

        cartesiam_plane(2000, 2000)
        self.controller.model.render_shapes()
       
        glFlush()

    def resize_window(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = width / height

        if(width >= height):
            gluOrtho2D(-1000 * aspect, 1000 * aspect, -1000, 1000)
        else:
            gluOrtho2D(-1000, 1000, -1000 / aspect, 1000 / aspect)

    def set_controller(self, controller):
        self.controller = controller
