from tkinter import *
from OpenGL.GL import *


from shape import Shape
from utils.shape_factory import ShapeFactory

from components.line_popup_frame import LineFrame
from components.circle_popup_frame import CircleFrame
from components.matriz_frame import MatrizFrame

from src.algorithms.DDA import drawLineDDA
from src.algorithms.PontoMedio import drawLineMP
from src.algorithms.circle_midpoint import draw_circleMP
from src.algorithms.circle_polynomial import draw_circle_polynomial
from src.algorithms.circle_trigonometric import draw_circle_trigonometric

from src.models.gl_window_model import singleton


class ContextMenuController:
    def __init__(self, view):
        self.model = singleton
        self.view = view

        self.view.shapes_sub_menu.add_command(label="Triangle",      command=lambda:self.create_shape(1))
        self.view.shapes_sub_menu.add_command(label="Square",        command=lambda:self.create_shape(2))
        self.view.shapes_sub_menu.add_command(label="Rectangle",     command=lambda:self.create_shape(3))
        self.view.shapes_sub_menu.add_command(label="New", command=self.do_not)
        self.view.shapes_sub_menu.add_command(label="info", command=self.do_not)

        self.view.lines_sub_menu.add_command(label="DDA", command=self.do_not)
        self.view.lines_sub_menu.add_command(label="MidPoint", command=self.do_not)

        self.view.circle_sub_menu.add_command(label="Trigonometric", command=self.do_not)
        self.view.circle_sub_menu.add_command(label="Polynomial", command=self.do_not)
        self.view.circle_sub_menu.add_command(label="MidPoint", command=self.do_not)
        
    def create_shape(self, type: str):
        match type:
            case 1:
                shape = ShapeFactory.triangle()
            case 2:
                shape = ShapeFactory.square()
            case 3:
                shape = ShapeFactory.rectangle()
            case _:
                print("Nenuma forma foi selecionada")
        self.model.add_shape(shape)
    
    #rever
    def new_shape(self):
        matriz_frame = MatrizFrame(self.gl_window)
        matriz_frame.open_popup()

        self.gl_window.wait_window(matriz_frame.popup)

        shape = ShapeFactory.default_shape(matriz_frame.input)

        self.model.add_shape(shape)

    #rever
    def create_line(self, drawline):
        lineFrame = LineFrame(self.gl_window)
        lineFrame.open_popup()

        self.gl_window.wait_window(lineFrame.popup)

        points = drawline(
            x1=lineFrame.x1,
            y1=lineFrame.y1,
            x2=lineFrame.x2,
            y2=lineFrame.y2
        )
        
        shape = Shape(points, GL_POINTS)

        self.gl_window.add_shape(shape)

    #rever
    def create_circle(self, draw_circle):
        circleFrame = CircleFrame(self.gl_window)
        circleFrame.open_popup()

        self.gl_window.wait_window(circleFrame.popup)
        
        points = draw_circle(circleFrame.radian)

        shape = Shape(points, GL_POINTS)

        self.gl_window.add_shape(shape)

    def do_not(self):
        pass

