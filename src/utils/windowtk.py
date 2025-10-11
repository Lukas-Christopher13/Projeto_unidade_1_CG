from typing import List

from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from .shape import Shape
from backgrounds import cartesiam_plane

#singleton
class WindowTk(OpenGLFrame):
    shapes: List[Shape] = []
    listeners = []
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._render = lambda: None
        self._init_config = lambda: None
        
    def initgl(self):
        glClearColor (1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(-1000, 1000, -1000, 1000) # Passar esse valor
        glMatrixMode (GL_MODELVIEW)

        glClearColor(1, 1, 1, 1)

    def redraw(self):
        width = self.winfo_width()
        height = self.winfo_height()
        aspect = width / height

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.resize_window(width, height)

        cartesiam_plane(width * aspect, height * aspect)
        for shape in self.shapes:
            shape.render()

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
                
    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
        self.notify()

    #delete e remover da lista
    def clear_all(self):
        for shape in self.shapes:
            shape.clear() 

    def delete_shape(self):
        shape = self.shapes[self.selected]
        shape.clear()

        self.shapes.remove(shape)
        self.notify()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify(self):
        for listener in self.listeners:
            listener.update()

    def set_selected(self, selected: int):
        self.selected = selected

    def get_selected(self):
        return self.shapes[self.selected]
    
    def print_info(self):
        print(self.width)
        print(self.height)
