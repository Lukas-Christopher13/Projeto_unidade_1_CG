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
        self.content_frame = Frame(self)
        self.content_frame.pack(fill=BOTH, expand=True)

        self.gl_container = Frame(self.content_frame, bd=0, highlightthickness=0)
        self.gl_container.pack(side=LEFT, fill=BOTH, expand=True)

        self.gl_window_view = GlWindowView(self.gl_container, bd=0, highlightthickness=0)
        self.gl_window_view.pack(fill=BOTH, expand=True, padx=0, pady=0)

        self.lateral_bar_view = LateralBarView(self.content_frame)
        self.lateral_bar_view.pack(side=LEFT, fill=BOTH, padx=0, pady=0)

        self.terminal_frame = TerminalFrame(
            self.gl_container,
            bd=0,
            relief="flat",
        )
        self.terminal_frame.attach_overlay(self.gl_container)

        # ── Context menu (vinculado ao GL) ──
        self.context_menu_view = ContextMenuView(self.gl_window_view)
