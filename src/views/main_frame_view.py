from tkinter import *

from src.views.gl_window_view import GlWindowView
from src.views.context_menu_view import ContextMenuView
from src.views.lateralbar_frame_view import LateralBarView
from src.components.terminal_frame import TerminalFrame


class MainFrameView(Frame):
    DEFAULT_TERMINAL_HEIGHT = 220
    MINIMIZED_TERMINAL_HEIGHT = 28
    EXPANDED_TERMINAL_RATIO = 0.30
    MIN_CANVAS_VISIBLE_HEIGHT = 180

    def __init__(self, parent, controller, **kwargs):  # adicionar controller
        super().__init__(parent, **kwargs)
        self.controller = controller
        self._terminal_state = "expanded"
        self._terminal_height = self.DEFAULT_TERMINAL_HEIGHT
        self._is_resizing_terminal = False
        self._resize_start_root_y = 0
        self._resize_start_height = self.DEFAULT_TERMINAL_HEIGHT
        self._drag_motion_binding = None
        self._drag_release_binding = None

        self.pack(fill="both", expand=True, padx=0, pady=0)
        self.build()

    def build(self):
        self.content_frame = Frame(self)
        self.content_frame.pack(fill=BOTH, expand=True)

        self.gl_area = Frame(self.content_frame, bg="#ffffff")
        self.gl_area.pack(side=LEFT, fill=BOTH, expand=True)
        self.gl_area.bind("<Configure>", self._on_gl_area_configure)

        self.lateral_bar_view = LateralBarView(self.content_frame)
        self.lateral_bar_view.pack(side=RIGHT, fill=Y, padx=0, pady=0)

        self.gl_window_view = GlWindowView(self.gl_area, bd=0, highlightthickness=0)
        self.gl_window_view.pack(fill=BOTH, expand=True, padx=0, pady=0)

        self.terminal_frame = TerminalFrame(
            self.gl_area,
            on_toggle_minimize=self.toggle_terminal,
            on_resize_start=self._start_terminal_resize,
            bd=1,
            relief="solid",
        )

        self.after_idle(self._apply_default_terminal_layout)

        self.context_menu_view = ContextMenuView(self.gl_window_view, self.controller)

    def toggle_terminal(self):
        if self._terminal_state == "minimized":
            self._expand_terminal()
            return

        self._cancel_terminal_resize()
        self._terminal_state = "minimized"
        self.terminal_frame.set_view_state(is_minimized=True)
        self.terminal_frame.set_collapsed(True)
        self.terminal_frame.set_resizable(False)
        self.after_idle(self._apply_terminal_layout)

    def _expand_terminal(self):
        self._terminal_state = "expanded"
        self.terminal_frame.set_view_state(is_minimized=False)
        self.terminal_frame.set_collapsed(False)
        self.terminal_frame.set_resizable(True)
        self._terminal_height = self._get_default_terminal_height()
        self.after_idle(self._apply_terminal_layout)

    def _apply_default_terminal_layout(self):
        self._terminal_state = "expanded"
        self.terminal_frame.set_view_state(is_minimized=False)
        self.terminal_frame.set_collapsed(False)
        self.terminal_frame.set_resizable(True)
        self._terminal_height = self._get_default_terminal_height()
        self._apply_terminal_layout()

    def _get_default_terminal_height(self):
        total_height = self.gl_area.winfo_height()
        if total_height <= 1:
            return self.DEFAULT_TERMINAL_HEIGHT

        return max(
            self.DEFAULT_TERMINAL_HEIGHT,
            int(total_height * self.EXPANDED_TERMINAL_RATIO),
        )

    def _get_max_terminal_height(self):
        total_height = self.gl_area.winfo_height()
        if total_height <= 1:
            return self.DEFAULT_TERMINAL_HEIGHT

        return max(
            self.MINIMIZED_TERMINAL_HEIGHT,
            total_height - self.MIN_CANVAS_VISIBLE_HEIGHT,
        )

    def _apply_terminal_layout(self):
        total_height = self.gl_area.winfo_height()
        if total_height <= 1:
            self.after(30, self._apply_terminal_layout)
            return

        if self._terminal_state == "minimized":
            height = self.MINIMIZED_TERMINAL_HEIGHT
        else:
            height = max(
                self.MINIMIZED_TERMINAL_HEIGHT,
                min(self._terminal_height, self._get_max_terminal_height()),
            )
            self._terminal_height = height

        self.terminal_frame.place(
            relx=0.0,
            rely=1.0,
            relwidth=1.0,
            x=0,
            y=0,
            anchor="sw",
            height=height,
        )
        self.terminal_frame.lift()

    def _on_gl_area_configure(self, _event):
        if self._terminal_state == "expanded":
            self._terminal_height = min(self._terminal_height, self._get_max_terminal_height())

        self._apply_terminal_layout()

    def _start_terminal_resize(self, event):
        if self._terminal_state != "expanded":
            return

        self._is_resizing_terminal = True
        self._resize_start_root_y = event.y_root
        self._resize_start_height = self._terminal_height
        toplevel = self.winfo_toplevel()
        self._drag_motion_binding = toplevel.bind("<B1-Motion>", self._on_terminal_resize_drag, add="+")
        self._drag_release_binding = toplevel.bind("<ButtonRelease-1>", self._stop_terminal_resize, add="+")

    def _on_terminal_resize_drag(self, event):
        if not self._is_resizing_terminal:
            return

        delta = self._resize_start_root_y - event.y_root
        self._terminal_height = self._resize_start_height + delta
        self._apply_terminal_layout()

    def _stop_terminal_resize(self, _event):
        if not self._is_resizing_terminal:
            return

        self._is_resizing_terminal = False
        self._cancel_terminal_resize()

    def _cancel_terminal_resize(self):
        self._is_resizing_terminal = False
        toplevel = self.winfo_toplevel()
        if self._drag_motion_binding is not None:
            toplevel.unbind("<B1-Motion>", self._drag_motion_binding)
            self._drag_motion_binding = None
        if self._drag_release_binding is not None:
            toplevel.unbind("<ButtonRelease-1>", self._drag_release_binding)
            self._drag_release_binding = None
