from tkinter import *

from utils.shape import Shape

class ContextMenu(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.contexte_menu = Menu(parent, tearoff=0)
        self.sub_menu = Menu(self.contexte_menu, tearoff=0)

        self.sub_menu.add_command(label="Pixel", command=self.command)
        self.sub_menu.add_command(label="Line (DDA)", command=self.command)
        self.sub_menu.add_command(label="Line (PM)", command=self.command)
        self.sub_menu.add_command(label="Triangle", command=self.command)
        self.sub_menu.add_command(label="Square", command=self.command)
        
        self.contexte_menu.add_cascade(label="shapes", menu=self.sub_menu)

        self.parent.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        self.contexte_menu.tk_popup(event.x_root, event.y_root)

    def create_shape(self):
        
        pass

    def create_triangle(self):
        tringle = [
            [-0.75,  1.0, 0.0, 1.0],
            [-1.0,   0.5, 0.0, 1.0],
            [-0.5,   0.5, 0.0, 1.0]
        ]

        self.parent.add_shape(Shape(tringle))

    def command():
        pass


