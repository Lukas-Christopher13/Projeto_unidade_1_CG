from tkinter import *

from src.controllers.context_menu_controller import ContextMenuController

class ContextMenuView(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.context_menu = Menu(root, tearoff=0)

        self.shapes_sub_menu = Menu(self.context_menu, tearoff=0)
        self.lines_sub_menu = Menu(self.context_menu, tearoff=0)
        self.circle_sub_menu = Menu(self.context_menu, tearoff=0)
        
        self.context_menu.add_cascade(label="Shapes", menu=self.shapes_sub_menu)
        self.context_menu.add_cascade(label="Lines", menu=self.lines_sub_menu)
        self.context_menu.add_cascade(label="Circles", menu=self.circle_sub_menu)
        
        root.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)
