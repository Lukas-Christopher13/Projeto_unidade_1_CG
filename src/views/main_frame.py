from tkinter import *

from src.utils.windowtk import WindowTk
from src.components.shapes_lateral_bar_frame import ShapesLateralBar
from src.components.contexte_menu_frame import ContextMenu

class MainFrame(Frame):
    def __init__(self, root, **kwargs): #adicionar controller
        super().__init__(root, **kwargs)

        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.gl_window = WindowTk(self, bd=0, highlightthickness=0)
        self.gl_window.pack(side=LEFT, expand=True, fill=BOTH, padx=0, pady=0)

        self.lateral_bar = ShapesLateralBar(self)
        self.lateral_bar.pack(side=LEFT)

        self.context_menu = ContextMenu(self)

        self.gl_window.animate = 1
        self.gl_window.mainloop()
 

