from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from utils.backgrounds import cartesiam_plane
from src.models.gl_window_model import singleton
from src.models.shape import Shape

from src.utils.pipeline_3d import Pipeline3D
from src.utils.shape_factory_3d import ShapeFactory3D

singleton.use_3d_axies()
singleton.add_shape(ShapeFactory3D.cube())

class GlWindowView(OpenGLFrame):
    window_mode = "2d"

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        
    def initgl(self):
        glClearColor (1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(-1000, 1000, -1000, 1000) # Passar esse valor
        glMatrixMode (GL_MODELVIEW)

        glClearColor(1, 1, 1, 1)

    def redraw(self):
        if self.window_mode == "3d":
            self.redraw_2d()
        else:
            self.redraw_3d()

    def redraw_2d(self):
        width = self.winfo_width()
        height = self.winfo_height()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.resize_window(width, height)

        cartesiam_plane(2000, 2000)
        self.controller.model.render_shapes()
       
        glFlush()

    def redraw_3d(self):
        width = self.winfo_width()
        height = self.winfo_height()

        self.pipeline_3d = Pipeline3D(
            width=width,
            height=height,
            x_min=0,
            y_min=0
        )

        self.display_3d()
    
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

    
    def display_3d(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for background in singleton.backgrounds:
            self.draw_3d(background)

        for shape in singleton.shapes:
            self.draw_3d(shape)

        glFlush()

    def draw_3d(self, shape):
        points = self.pipeline_3d.transform(shape.vertex)

        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(2)
        glBegin(GL_LINES)
        if  shape.has_edge_sequence():
            for a, b in shape.edge_sequence:
                glVertex2f(points[a][0], points[a][1])
                glVertex2f(points[b][0], points[b][1])
        else:
            for point in points:
                glVertex2f(point[0], point[1])
        glEnd()
