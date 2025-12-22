from tkinter import *

from src.views.gl_window_view import GlWindowView
from src.views.context_menu_view import ContextMenuView
from src.views.lateralbar_frame_view import LateralBarView


class MainFrameView(Frame):
    def __init__(self, parent, controller, **kwargs): #adicionar controller
        super().__init__(parent, **kwargs)
        self.controller = controller
         
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.gl_window_view = GlWindowView(self, bd=0, highlightthickness=0)
        self.gl_window_view.pack(side=LEFT, expand=True, fill=BOTH, padx=0, pady=0)

        self.lateral_bar_view = LateralBarView(self, self.gl_window_view)
        self.lateral_bar_view.pack(side=LEFT, fill=BOTH, padx=0, pady=0)

        self.context_menu_view = ContextMenuView(self.gl_window_view)

        


    

