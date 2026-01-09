import tkinter as tk
from tkinter import ttk
from tkinter import *

from src.models.gl_window_model import gl_window_model

class ViewModeView(Frame):
    def __init__(self, master):
        super().__init__(master, padx=10, pady=10)

        tk.Label(self, text="Modo de Visualização", font=("Arial", 10, "bold")).pack(anchor="w")

        self.mode = tk.StringVar(value="2D")

        ttk.Radiobutton(
            self, text="2D",
            variable=self.mode, value="2D",
            command=gl_window_model.to_2d
        ).pack(anchor="w")

        ttk.Radiobutton(
            self, text="3D",
            variable=self.mode, value="3D",
            command=gl_window_model.to_3d
        ).pack(anchor="w")

    def on_change(self):
        print("Modo:", self.mode.get())
        print("Eixos:", self.show_axes.get())
        print("Grid:", self.show_grid.get())
        print("Zoom:", self.zoom.get())
        print("-" * 20)

    def set_controller(self, controller):
        self.controller = controller
