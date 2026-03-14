from src.models.gl_window_model import gl_window_model
from src.controllers.edit_shape_controller import EditShapeController
from src.models.shape import Shape
from OpenGL.GL import GL_POINTS, GL_LINE_STRIP
from src.services.render_service import RenderService
import numpy as np

class LateralBarController:
    def __init__(self, view, gl_window_controller, model):
        self.view = view
        self.model = model
        self.gl_window_controller = gl_window_controller

        self.edit_shape_controller = EditShapeController(self.view.edit_shape_view, None)

        gl_window_model.add_listener(self)
        self.view.set_point_actions(self.add_point_to_shape, self.new_shape)

        self._selected_line_algorithm = None
        self._selected_circle_algorithm = None
        self._editing_shape_index = None

    def _reset_scene_with_axes(self):
        gl_window_model.empty_window()
        gl_window_model.selected = None
        self._editing_shape_index = None
        self.view.set_points([])

        if gl_window_model.is_2d():
            gl_window_model.use_2d_axies()
        else:
            gl_window_model.use_3d_axies()

        RenderService.request_render()
        
    def update(self):
        if self._editing_shape_index is not None and self._editing_shape_index < len(gl_window_model.shapes):
            shape = gl_window_model.shapes[self._editing_shape_index]
            points = [v[:3] for v in shape.vertex]
            self.view.set_points(points)
            gl_window_model.set_selected(self._editing_shape_index)
            return

        if gl_window_model.selected is None and gl_window_model.shapes:
            gl_window_model.set_selected(len(gl_window_model.shapes) - 1)

        selected = gl_window_model.get_selected()
        if selected is None:
            self.view.set_points([])
            return

        points = [v[:3] for v in selected.vertex]
        self.view.set_points(points)

    def show_transform_screen(self):
        self._reset_scene_with_axes()
        self.view.show_transform_screen()

    def show_line_algorithm_screen(self, name: str, algorithm):
        self._reset_scene_with_axes()
        self._selected_line_algorithm = algorithm
        self.view.show_line_algorithm_screen(name)
        self.view.set_algorithm_action("Desenhar Linha", self._run_line_algorithm)

    def show_circle_algorithm_screen(self, name: str, algorithm):
        self._reset_scene_with_axes()
        self._selected_circle_algorithm = algorithm
        self.view.show_circle_algorithm_screen(name)
        self.view.set_algorithm_action("Desenhar Circulo", self._run_circle_algorithm)

    def _run_line_algorithm(self):
        if self._selected_line_algorithm is None:
            return

        values = self.view.get_line_inputs()
        if values is None:
            return

        points = self._selected_line_algorithm(
            x1=values["x1"],
            y1=values["y1"],
            x2=values["x2"],
            y2=values["y2"],
        )
        gl_window_model.add_shape(Shape(points, GL_POINTS))
        self._editing_shape_index = None

    def _run_circle_algorithm(self):
        if self._selected_circle_algorithm is None:
            return

        values = self.view.get_circle_inputs()
        if values is None:
            return

        points = self._selected_circle_algorithm(
            values["radian"],
            values["origin_x"],
            values["origin_y"],
        )
        gl_window_model.add_shape(Shape(points, GL_POINTS))
        self._editing_shape_index = None

    def new_shape(self):
        self._editing_shape_index = None
        self.view.set_points([])

    def add_point_to_shape(self):
        values = self.view.get_point_input()
        if values is None:
            return

        point = np.array([[values[0], values[1], values[2], 1.0]], dtype=np.float32)

        if self._editing_shape_index is None or self._editing_shape_index >= len(gl_window_model.shapes):
            shape = Shape(point.tolist(), GL_LINE_STRIP)
            gl_window_model.add_shape(shape)
            self._editing_shape_index = len(gl_window_model.shapes) - 1
            gl_window_model.set_selected(self._editing_shape_index)
        else:
            shape = gl_window_model.shapes[self._editing_shape_index]
            shape.update(GL_LINE_STRIP, point)
            RenderService.request_render()

        self.update()
        