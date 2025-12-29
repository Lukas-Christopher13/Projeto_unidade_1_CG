import tkinter as tk
from tkinter import ttk
from tkinter import *

from src.models.gl_window_model import gl_window_model

class ViewModeView(Frame):
    def __init__(self, master):
        super().__init__(master, padx=10, pady=10)

        # ===== MODO =====
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

        # ===== EXTRAS =====
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=5)

        tk.Label(self, text="Extras", font=("Arial", 10, "bold")).pack(anchor="w")

        self.show_axes = tk.BooleanVar(value=True)
        self.show_grid = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            self, text="Mostrar Eixos",
            variable=self.show_axes,
            command=self.on_change
        ).pack(anchor="w")

        ttk.Checkbutton(
            self, text="Mostrar Grid",
            variable=self.show_grid,
            command=self.on_change
        ).pack(anchor="w")

        # ===== ZOOM =====
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=5)

        tk.Label(self, text="Zoom").pack(anchor="w")

        self.zoom = tk.DoubleVar(value=1.0)
        ttk.Scale(
            self, from_=0.5, to=3.0,
            variable=self.zoom,
            command=lambda e: self.on_change()
        ).pack(fill="x")

    def on_change(self):
        print("Modo:", self.mode.get())
        print("Eixos:", self.show_axes.get())
        print("Grid:", self.show_grid.get())
        print("Zoom:", self.zoom.get())
        print("-" * 20)

    def set_controller(self, controller):
        self.controller = controller
