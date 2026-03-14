from tkinter import *
from OpenGL.GL import *

from src.models.shape import Shape
from controllers.custom_shape_controller import CustomShapeController
from src.utils.shape_factory import ShapeFactory
from src.utils.shape_factory_3d import ShapeFactory3D

from components.line_popup_frame import LineFrame
from components.circle_popup_frame import CircleFrame
from components.matriz_frame import MatrizFrame

from src.algorithms.DDA import drawLineDDA
from src.algorithms.PontoMedio import drawLineMP
from src.algorithms.circle_midpoint import draw_circleMP
from src.algorithms.circle_polynomial import draw_circle_polynomial
from src.algorithms.circle_trigonometric import draw_circle_trigonometric

from src.models.gl_window_model import gl_window_model


class ContextMenuController:
    def __init__(self, view):
        self.view = view
        self.custon_shape_controller = CustomShapeController(view)

    def options_2d(self):
        self.view.shapes_sub_menu.add_command(label="Traingle",      command=lambda:self.create_shape("triangle"))
        self.view.shapes_sub_menu.add_command(label="Square",        command=lambda:self.create_shape("square"))
        self.view.shapes_sub_menu.add_command(label="Rectangle",     command=lambda:self.create_shape("rectangle"))

        self.view.shapes_sub_menu.add_command(label="Custom",        command=self.custon_shape_controller.start_custom_shape) #-----------

        self.view.shapes_sub_menu.add_command(label="info", command=self.do_not)

        self.view.lines_sub_menu.add_command(label="DDA",            command=lambda:self.create_line(drawLineDDA))
        self.view.lines_sub_menu.add_command(label="MidPoint",       command=lambda:self.create_line(drawLineMP))

        self.view.circle_sub_menu.add_command(label="Trigonometric", command=lambda:self.create_circle(draw_circle_trigonometric))
        self.view.circle_sub_menu.add_command(label="Polynomial",    command=lambda:self.create_circle(draw_circle_polynomial))
        self.view.circle_sub_menu.add_command(label="MidPoint",      command=lambda:self.create_circle(draw_circleMP))
        
    def options_3d(self):
        self.view.shapes_sub_menu.add_command(label="Cube",      command=lambda:self.create_shape("cube"))
        self.view.shapes_sub_menu.add_command(label="CubeBug",   command=lambda:self.create_shape("cube_b"))
        self.view.shapes_sub_menu.add_command(label="Pyramid",   command=lambda:self.create_shape("pyramid"))
        
    def create_shape(self, shape_type: str):
        shape_map = {
            "triangle": ShapeFactory.triangle,
            "square": ShapeFactory.square,
            "rectangle": ShapeFactory.rectangle,
            "cube": ShapeFactory3D.cube,
            "cube_b":ShapeFactory3D.cube_bug,
            "pyramid": ShapeFactory3D.pyramidy
        }

        factory = shape_map.get(shape_type)

        if not factory:
            print("Nenhuma forma foi selecionada")
            return

        shape = factory()
        gl_window_model.add_shape(shape)

    def create_line(self, drawline):
        lineFrame = LineFrame(self.view)
        lineFrame.open_popup()

        self.view.wait_window(lineFrame.popup)

        if getattr(lineFrame, 'cancelled', False):
            return

        points = drawline(
            x1=lineFrame.x1,
            y1=lineFrame.y1,
            x2=lineFrame.x2,
            y2=lineFrame.y2
        )
        
        shape = Shape(points, GL_POINTS)

        gl_window_model.add_shape(shape)

    def create_circle(self, draw_circle):
        circleFrame = CircleFrame(self.view)
        circleFrame.open_popup()

        self.view.wait_window(circleFrame.popup)

        if getattr(circleFrame, 'cancelled', False):
            return
        
        points = draw_circle(
            circleFrame.radian,
            circleFrame.origin_x,
            circleFrame.origin_y
        )

        shape = Shape(points, GL_POINTS)

        gl_window_model.add_shape(shape)

    #rever
    def new_shape(self):
        matriz_frame = MatrizFrame(self.gl_window)
        matriz_frame.open_popup()

        self.gl_window.wait_window(matriz_frame.popup)

        shape = ShapeFactory.default_shape(matriz_frame.input)

        self.model.add_shape(shape)

    def do_not(self):
        pass
