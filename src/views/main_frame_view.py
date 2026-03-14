from tkinter import *

from src.views.gl_window_view import GlWindowView
from src.views.context_menu_view import ContextMenuView
from src.views.lateralbar_frame_view import LateralBarView
from src.components.terminal_frame import TerminalFrame

from src.models.gl_window_model import gl_window_model


class MainFrameView(Frame):
    def __init__(self, parent, controller, **kwargs): #adicionar controller
        super().__init__(parent, **kwargs)
        self.controller = controller
         
        self.pack(fill="both", expand=True, padx=0, pady=0)
        self.build()

    def build(self):
        # ── PanedWindow vertical: [canvas+lateral] / [terminal] ──
        self.paned = PanedWindow(self, orient=VERTICAL, sashwidth=6, bg="#cccccc")
        self.paned.pack(fill=BOTH, expand=True)

        # ── Painel superior: GL + lateral bar ──
        top_frame = Frame(self.paned)

        self.gl_window_view = GlWindowView(top_frame, bd=0, highlightthickness=0)
        self.gl_window_view.pack(side=LEFT, expand=True, fill=BOTH, padx=0, pady=0)

        self.lateral_bar_view = LateralBarView(top_frame)
        self.lateral_bar_view.pack(side=LEFT, fill=BOTH, padx=0, pady=0)

        self.paned.add(top_frame, stretch="always")

        # ── Painel inferior: Terminal de logs ──
        self.terminal_frame = TerminalFrame(self.paned)
        self.paned.add(self.terminal_frame, height=220, stretch="never")

        # ── Context menu (vinculado ao GL) ──
        self.context_menu_view = ContextMenuView(self.gl_window_view)
