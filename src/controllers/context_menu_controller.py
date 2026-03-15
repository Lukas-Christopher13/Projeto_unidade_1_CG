from tkinter import *
from src.components.cohen_sutherland_popup_frame import CohenSutherlandClipFrame

from src.algorithms.DDA import drawLineDDA
from src.algorithms.PontoMedio import drawLineMP
from src.algorithms.circle_midpoint import draw_circleMP
from src.algorithms.circle_polynomial import draw_circle_polynomial
from src.algorithms.circle_trigonometric import draw_circle_trigonometric
from src.utils.shape_factory import ShapeFactory
from src.utils.shape_factory_3d import ShapeFactory3D
from src.controllers.custom_shape_controller import CustomShapeController

from src.models.gl_window_model import gl_window_model


class ContextMenuController:
    def __init__(self, view, app_controller=None):
        self.view = view
        self.app_controller = app_controller
        self.custom_shape_controller = CustomShapeController(view)

    def options_2d(self):
        self.view.lines_sub_menu.add_radiobutton(
            label="DDA",
            variable=self.view.screen_state,
            value="line_dda",
            command=lambda: self.open_line_screen("DDA", drawLineDDA, "line_dda")
        )
        self.view.lines_sub_menu.add_radiobutton(
            label="MidPoint",
            variable=self.view.screen_state,
            value="line_midpoint",
            command=lambda: self.open_line_screen("MidPoint", drawLineMP, "line_midpoint")
        )

        self.view.circle_sub_menu.add_radiobutton(
            label="Trigonometric",
            variable=self.view.screen_state,
            value="circle_trigonometric",
            command=lambda: self.open_circle_screen("Trigonometric", draw_circle_trigonometric, "circle_trigonometric")
        )
        self.view.circle_sub_menu.add_radiobutton(
            label="Polynomial",
            variable=self.view.screen_state,
            value="circle_polynomial",
            command=lambda: self.open_circle_screen("Polynomial", draw_circle_polynomial, "circle_polynomial")
        )
        self.view.circle_sub_menu.add_radiobutton(
            label="MidPoint",
            variable=self.view.screen_state,
            value="circle_midpoint",
            command=lambda: self.open_circle_screen("MidPoint", draw_circleMP, "circle_midpoint")
        )

    def mount_click_shapes_menu(self):
        self.view.click_shapes_menu.add_command(label="Triangulo", command=lambda: self.create_shape("triangle"))
        self.view.click_shapes_menu.add_command(label="Quadrado", command=lambda: self.create_shape("square"))
        self.view.click_shapes_menu.add_command(label="Retangulo", command=lambda: self.create_shape("rectangle"))
        self.view.click_shapes_menu.add_separator()
        self.view.click_shapes_menu.add_command(label="Custom", command=self.custom_shape_controller.start_custom_shape)

    def mount_click_shapes_menu_3d(self):
        self.view.click_shapes_menu.add_command(label="Cube", command=lambda: self.create_shape("cube"))
        self.view.click_shapes_menu.add_command(label="CubeBug", command=lambda: self.create_shape("cube_b"))
        self.view.click_shapes_menu.add_command(label="Pyramid", command=lambda: self.create_shape("pyramid"))

    def options_3d(self):
        # Em 3D, os algoritmos 2D de linha/circulo ficam indisponiveis.
        self.view.lines_sub_menu.add_command(label="Indisponivel em 3D", state=DISABLED)
        self.view.circle_sub_menu.add_command(label="Indisponivel em 3D", state=DISABLED)

    def mount_transform_menu(self):
        self.view.transform_sub_menu.add_radiobutton(
            label="2D",
            variable=self.view.screen_state,
            value="transform_2d",
            command=self.go_2d
        )
        self.view.transform_sub_menu.add_radiobutton(
            label="3D",
            variable=self.view.screen_state,
            value="transform_3d",
            command=self.go_3d
        )

    def open_line_clip_popup(self):
        clip_frame = CohenSutherlandClipFrame(
            self.view,
            title="Recorte de Reta - Cohen-Sutherland",
            w=980,
            h=720
        )
        clip_frame.open_popup()
        self.view.wait_window(clip_frame.popup)

    def open_line_screen(self, name: str, algorithm, state_key: str):
        if self.app_controller is None:
            return
        self.view.set_screen_state(state_key)
        self.app_controller.show_line_algorithm_screen(name, algorithm)

    def open_circle_screen(self, name: str, algorithm, state_key: str):
        if self.app_controller is None:
            return
        self.view.set_screen_state(state_key)
        self.app_controller.show_circle_algorithm_screen(name, algorithm)

    def go_2d(self):
        self.view.after_idle(lambda: self._apply_mode_change("2d"))

    def go_3d(self):
        self.view.after_idle(lambda: self._apply_mode_change("3d"))

    def _apply_mode_change(self, mode: str):
        if mode == "2d":
            gl_window_model.to_2d()
            self.view.set_screen_state("transform_2d")
        else:
            gl_window_model.to_3d()
            self.view.set_screen_state("transform_3d")

        if self.app_controller is not None:
            self.app_controller.show_transform_screen(reset_scene=False)

    def create_shape(self, shape_type: str):
        shape_map = {
            "triangle": ShapeFactory.triangle,
            "square": ShapeFactory.square,
            "rectangle": ShapeFactory.rectangle,
            "cube": ShapeFactory3D.cube,
            "cube_b": ShapeFactory3D.cube_bug,
            "pyramid": ShapeFactory3D.pyramidy,
        }

        factory = shape_map.get(shape_type)
        if not factory:
            return

        gl_window_model.set_single_shape(factory())
