from tkinter import *

from src.utils.windowtk import WindowTk
from src.shape_factory import ShapeFactory

class ContextMenu(Frame):
    def __init__(self, gl_window: WindowTk, **kwargs):
        super().__init__(gl_window, **kwargs)
        self.gl_window = gl_window

        self.context_menu = Menu(gl_window, tearoff=0)
        self.sub_menu = Menu(self.context_menu, tearoff=0)
        
        self.sub_menu.add_command(label="Triangle", command=lambda: self.create_shape(1))
        self.sub_menu.add_command(label="Square", command=lambda: self.create_shape(2))
        self.sub_menu.add_command(label="Rectangle", command=lambda: self.create_shape(3))
        self.sub_menu.add_command(label="info", command=self.command)
        
        self.context_menu.add_cascade(label="Shapes", menu=self.sub_menu)
        

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


