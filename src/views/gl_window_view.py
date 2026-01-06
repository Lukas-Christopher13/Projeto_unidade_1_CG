from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *

from src.utils.pipeline_2d import Pipeline2D
from src.utils.pipeline_3d import Pipeline3D
from src.services.render_service import RenderService
from src.models.gl_window_model import gl_window_model


class GlWindowView(OpenGLFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        RenderService.register_view(self)

        self.animate = 0
        
    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)

    def redraw(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.aspect = self.width / self.height

        if gl_window_model.get_window_mode() == "2d":
            self.redraw_2d()
        else:
            self.redraw_3d()

    def request_render(self):
        self.event_generate("<Expose>")

    def redraw_2d(self):
        self.pipeline_2d = Pipeline2D(
            viewport_xmin = 0,
            viewport_ymin = 0,
            viewport_xmax= self.width,
            viewport_ymax= self.height
        )

        self.display_2d()

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
    
    def display_2d(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for background in gl_window_model.backgrounds:
            background.render(self.pipeline_2d)

        for shape in gl_window_model.shapes:
            shape.render(self.pipeline_2d)

        glFlush()
    
    def display_3d(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        for background in gl_window_model.backgrounds:
            background.render_3d(self.pipeline_3d)

        for shape in gl_window_model.shapes:
            shape.render_3d(self.pipeline_3d)

        glFlush()

    def set_controller(self, controller):
        self.controller = controller
