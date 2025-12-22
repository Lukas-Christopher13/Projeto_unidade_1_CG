from tkinter import *
from src.utils.windowtk import WindowTk
from src.views.lateralbar_frame_view import LateralBarView

class MainFrameView(Frame):
    def __init__(self, parent, controller, **kwargs): #adicionar controller
        super().__init__(parent, **kwargs)
        self.controller = controller
         
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.gl_window = WindowTk(self, bd=0, highlightthickness=0)
        self.gl_window.pack(side=LEFT, expand=True, fill=BOTH, padx=0, pady=0)

        self.lateral_bar_view = LateralBarView(self, self.gl_window)
        self.lateral_bar_view.pack(side=LEFT, fill=BOTH, padx=0, pady=0)


    

