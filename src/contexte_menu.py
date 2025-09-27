from tkinter import *

from utils.shape import Shape

class ContextMenu(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.context_menu = Menu(parent, tearoff=0)
        self.context_menu.add_command(label="Triangulo", command=self.create_triangle)
        self.context_menu.add_command(label="retas", command=self.command)
        self.context_menu.add_command(label="tranformaçẽos", command=self.command)
        self.context_menu.add_command(label="definir ponto", command=self.command)
        self.context_menu.add_command(label="3D", command=self.command)

        self.parent.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def create_triangle(self):
        tringle = [
            [-0.75,  1.0, 0.0, 1.0],
            [-1.0,   0.5, 0.0, 1.0],
            [-0.5,   0.5, 0.0, 1.0]
        ]

        self.parent.add_shape(Shape(tringle))

    def command():
        pass


