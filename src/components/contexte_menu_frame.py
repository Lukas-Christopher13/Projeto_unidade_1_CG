from tkinter import *
from OpenGL.GL import *

from src.utils.windowtk import WindowTk

from shape import Shape
from utils.shape_factory import ShapeFactory

from components.line_popup_frame import LineFrame
from components.circle_popup_frame import CircleFrame

from src.algorithms.DDA import drawLineDDA
from src.algorithms.PontoMedio import drawLineMP
from src.algorithms.circle_midpoint import draw_circleMP

class ContextMenu(Frame):
    def __init__(self, gl_window: WindowTk, **kwargs):
        super().__init__(gl_window, **kwargs)
        self.gl_window = gl_window

        self.context_menu = Menu(gl_window, tearoff=0)

        self.shapes_sub_menu = Menu(self.context_menu, tearoff=0)
        self.lines_sub_menu = Menu(self.context_menu, tearoff=0)
        self.circle_sub_menu = Menu(self.context_menu, tearoff=0)
        
        self.shapes_sub_menu.add_command(label="Triangle", command=lambda: self.create_shape(1))
        self.shapes_sub_menu.add_command(label="Square", command=lambda: self.create_shape(2))
        self.shapes_sub_menu.add_command(label="Rectangle", command=lambda: self.create_shape(3))
        self.shapes_sub_menu.add_command(label="info", command=self.command)

        self.lines_sub_menu.add_command(label="DDA", command=lambda: self.create_line(drawLineDDA))
        self.lines_sub_menu.add_command(label="MidPoint", command=lambda: self.create_line(drawLineMP))

        self.circle_sub_menu.add_command(label="MidPoint", command=lambda: self.create_circle())
        
        self.context_menu.add_cascade(label="Shapes", menu=self.shapes_sub_menu)
        self.context_menu.add_cascade(label="Lines", menu=self.lines_sub_menu)
        self.context_menu.add_cascade(label="Circles", menu=self.circle_sub_menu)
        

        self.gl_window.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

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
        self.gl_window.add_shape(shape)

    def command(self):
        self.gl_window.print_info()

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

    def create_circle(self):
        circleFrame = CircleFrame(self.gl_window)
        circleFrame.open_popup()

        self.gl_window.wait_window(circleFrame.popup)
        
        points = draw_circleMP(circleFrame.radian)

        shape = Shape(points, GL_POINTS)

        self.gl_window.add_shape(shape)
        

