import numpy as np

from OpenGL.GL import *

from src.models.shape import Shape
from src.utils.pipeline_2d import Pipeline2D
from src.services.render_service import RenderService
from src.models.gl_window_model import gl_window_model


class CustomShapeController:
    def __init__(self, view):
        self.view = view 
        self.custom_shape = None   
        self.custom_mode = False
        self.custom_points = []

    def start_custom_shape(self):
        if not gl_window_model.is_2d():
            return

        self.custom_mode = True
        self.custom_points = []
        self.custom_shape = None

        
        self.view.root.config(cursor="cross")

        self.view.root.bind("<Button-1>", self.add_custom_point)
        self.view.root.bind("<Button-3>", self.finish_custom_shape)

    def add_custom_point(self, event):
        if not self.custom_mode:
            return

        width = max(1, self.view.root.winfo_width())
        height = max(1, self.view.root.winfo_height())
        pipeline = Pipeline2D(0, 0, width, height)

        x_view = event.x
        y_view = height - event.y

        x_world, y_world = pipeline.viewport_to_world(x_view, y_view)
        point = np.array([[x_world, y_world, 0.0, 1.0]], dtype=np.float32)

        self.custom_points.append(point[0].tolist())

        if self.custom_shape is None:
            self.custom_shape = Shape(self.custom_points, GL_LINE_LOOP)
            gl_window_model.set_single_shape(self.custom_shape)
            gl_window_model.set_selected(0)
        else:
            self.custom_shape.update(GL_LINE_LOOP, point)
            gl_window_model.notify()
            RenderService.request_render()

    def finish_custom_shape(self, event):
        if not self.custom_mode:
            return

        self.custom_mode = False
        self.view.root.unbind("<Button-1>")
        self.view.root.bind("<Button-3>", self.view.show_click_menu)

        if len(self.custom_points) < 2:
            self.custom_shape = None
            self.custom_points = []
            self.view.root.config(cursor="")
            RenderService.request_render()
            return "break"

        self.custom_shape = None
        self.custom_points = []
        
        self.view.root.config(cursor="")

        RenderService.request_render()
        return "break"
