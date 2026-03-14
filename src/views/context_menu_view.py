from tkinter import *

from src.models.gl_window_model import gl_window_model
from src.controllers.context_menu_controller import ContextMenuController

class ContextMenuView(Frame):
    def __init__(self, root, app_controller=None, **kwargs):
        super().__init__(root, **kwargs)

        self.root = root
        self.toplevel = self.root.winfo_toplevel()
        self.context_menu_controller = ContextMenuController(self, app_controller)
        self.screen_state = StringVar(value="transform_2d")

        self.menu_bar = None

        self.rebuild()

        gl_window_model.add_frame(self)

    def build_2d_menu(self):
        self.screen_state.set("transform_2d")
        self.menu_bar = Menu(self.toplevel)
        self.algorithms_menu = Menu(self.menu_bar, tearoff=0)
        self.lines_sub_menu = Menu(self.algorithms_menu, tearoff=0)
        self.circle_sub_menu = Menu(self.algorithms_menu, tearoff=0)

        self.algorithms_menu.add_cascade(label="Linha", menu=self.lines_sub_menu)
        self.algorithms_menu.add_cascade(label="Circulo", menu=self.circle_sub_menu)
        self.menu_bar.add_cascade(label="Algoritmos", menu=self.algorithms_menu)

        self.transform_sub_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Transformacoes", menu=self.transform_sub_menu)
        self.menu_bar.add_command(label="Recorte de tela", command=self.context_menu_controller.open_line_clip_popup)

        self.context_menu_controller.options_2d()
        self.context_menu_controller.mount_transform_menu()

        self.click_menu = Menu(self.root, tearoff=0)
        self.click_shapes_menu = Menu(self.click_menu, tearoff=0)
        self.click_menu.add_cascade(label="Formas", menu=self.click_shapes_menu)
        self.context_menu_controller.mount_click_shapes_menu()
        self.root.bind("<Button-3>", self.show_click_menu)

        self.toplevel.config(menu=self.menu_bar)

    def build_3d_menu(self):
        self.screen_state.set("transform_3d")
        self.menu_bar = Menu(self.toplevel)
        self.algorithms_menu = Menu(self.menu_bar, tearoff=0)
        self.lines_sub_menu = Menu(self.algorithms_menu, tearoff=0)
        self.circle_sub_menu = Menu(self.algorithms_menu, tearoff=0)

        self.algorithms_menu.add_cascade(label="Linha", menu=self.lines_sub_menu)
        self.algorithms_menu.add_cascade(label="Circulo", menu=self.circle_sub_menu)
        self.menu_bar.add_cascade(label="Algoritmos", menu=self.algorithms_menu)

        self.transform_sub_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Transformacoes", menu=self.transform_sub_menu)
        self.menu_bar.add_command(label="Recorte de tela", command=self.context_menu_controller.open_line_clip_popup)

        self.context_menu_controller.options_3d()
        self.context_menu_controller.mount_transform_menu()

        self.click_menu = None
        self.root.unbind("<Button-3>")

        self.toplevel.config(menu=self.menu_bar)

    def rebuild(self):
        self.menu_bar = None

        if gl_window_model.is_2d():
            self.build_2d_menu()
        else:
            self.build_3d_menu()

    def set_screen_state(self, state: str):
        self.screen_state.set(state)

    def show_click_menu(self, event):
        if gl_window_model.is_2d() and self.click_menu is not None:
            self.click_menu.tk_popup(event.x_root, event.y_root)
