from typing import List

from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *

from .shape import Shape

#singleton
class WindowTk(OpenGLFrame):
    shapes: List[Shape] = []
    listeners = []
    backgrounds = []
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._render = lambda: None
        self._init_config = lambda: None
        
    def initgl(self):
        glClearColor(1, 1, 1, 1)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for background in self.backgrounds:
            background()

        for shape in self.shapes:
            shape.render()

        glFlush()

    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
        self.notify()

    def add_background(self, background):
        self.backgrounds.append(background)

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
