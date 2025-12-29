from tkinter import *

from src.models.gl_window_model import gl_window_model
from src.controllers.context_menu_controller import ContextMenuController

class ContextMenuView(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self.root = root
        self.context_menu_controller = ContextMenuController(self)

        self.context_menu = None

        self.rebuild()

        self.root.bind("<Button-3>", self.show_menu)

        gl_window_model.add_frame(self)

    def build_2d_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)

        self.shapes_sub_menu = Menu(self.context_menu, tearoff=0)
        self.lines_sub_menu = Menu(self.context_menu, tearoff=0)
        self.circle_sub_menu = Menu(self.context_menu, tearoff=0)

        self.context_menu.add_cascade(label="Shapes", menu=self.shapes_sub_menu)
        self.context_menu.add_cascade(label="Lines", menu=self.lines_sub_menu)
        self.context_menu.add_cascade(label="Circles", menu=self.circle_sub_menu)

        self.context_menu_controller.options_2d()

    def build_3d_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)

        self.shapes_sub_menu = Menu(self.context_menu, tearoff=0)
        self.context_menu.add_cascade(label="Shapes", menu=self.shapes_sub_menu)

        self.context_menu_controller.options_3d()

    def show_menu(self, event):
        if self.context_menu:
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def rebuild(self):
        self.context_menu = None

        if gl_window_model.is_2d():
            self.build_2d_menu()
        else:
            self.build_3d_menu()
