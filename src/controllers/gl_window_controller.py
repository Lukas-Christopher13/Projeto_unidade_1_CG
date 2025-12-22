from tkinter import *
from OpenGL.GL import *
from OpenGL.GLU import *

from src.models.gl_window_model import singleton

class GlWindowController:
    def __init__(self, view):
        self.model = singleton

        self.view = view
        self.view.set_controller(self)

    def resize_window(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = width / height

        if(width >= height):
            gluOrtho2D(-1000 * aspect, 1000 * aspect, -1000, 1000)
        else:
            gluOrtho2D(-1000, 1000, -1000 / aspect, 1000 / aspect)

        