from tkinter import *
import tkinter as tk
from tkinter import ttk

from src.models.gl_window_model import gl_window_model
from src.views.inputs.abs_input_frame import ABSInputFrame

class ShareInputFrame(ABSInputFrame):
    def _form_content(self):
        self.rebuild()

        gl_window_model.add_frame(self)

    def rebuild(self):
        self.clear_content()

        if gl_window_model.is_2d():
            self._form_2d()
        else:
            self._form_3d()

        ttk.Button(self.content, command=self.command, text="Aplicar").grid(
            row=self._button_row, column=0, pady=10, sticky="ew"
        )
        ttk.Button(self.content, text="Reset").grid(
            row=self._button_row, column=1, pady=10, sticky="ew"
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _form_2d(self):
        self.shx_var = tk.StringVar(value="0.0")
        self.shy_var = tk.StringVar(value="0.0")
        self.mode_var = tk.StringVar(value="x")

        ttk.Label(self.content, text="Shx:").grid(row=0, column=0, sticky="w")
        ttk.Label(self.content, text="Shy:").grid(row=1, column=0, sticky="w")

        self.x_input = ttk.Entry(self.content, textvariable=self.shx_var, width=10)
        self.x_input.grid(row=0, column=1, padx=5)

        self.y_input = ttk.Entry(self.content, textvariable=self.shy_var, width=10)
        self.y_input.grid(row=1, column=1, padx=5)

        self.z_input = None

        ttk.Label(self.content, text="Modo:").grid(row=2, column=0, sticky="w", pady=(8, 0))

        ttk.Radiobutton(self.content, text="Shear X", variable=self.mode_var, value="x") \
            .grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Shear Y", variable=self.mode_var, value="y") \
            .grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Shear X + Y", variable=self.mode_var, value="xy") \
            .grid(row=4, column=1, sticky="w")

        self._button_row = 5

    def _form_3d(self):
        self.shx_var = tk.StringVar(value="0.0")
        self.shy_var = tk.StringVar(value="0.0")
        self.shz_var = tk.StringVar(value="0.0")
        self.mode_var = tk.StringVar(value="x")

        ttk.Label(self.content, text="Shx:").grid(row=0, column=0, sticky="w")
        ttk.Label(self.content, text="Shy:").grid(row=1, column=0, sticky="w")
        ttk.Label(self.content, text="Shz:").grid(row=2, column=0, sticky="w")

        self.x_input = ttk.Entry(self.content, textvariable=self.shx_var, width=10)
        self.x_input.grid(row=0, column=1, padx=5)

        self.y_input = ttk.Entry(self.content, textvariable=self.shy_var, width=10)
        self.y_input.grid(row=1, column=1, padx=5)

        self.z_input = ttk.Entry(self.content, textvariable=self.shz_var, width=10)
        self.z_input.grid(row=2, column=1, padx=5)

        ttk.Label(self.content, text="Modo:").grid(row=3, column=0, sticky="w", pady=(8, 0))

        ttk.Radiobutton(self.content, text="Shear X", variable=self.mode_var, value="x") \
            .grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Shear Y", variable=self.mode_var, value="y") \
            .grid(row=4, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Shear Z", variable=self.mode_var, value="z") \
            .grid(row=5, column=1, sticky="w")

        self._button_row = 6

    def get(self):
        try:
            x = float(self.x_input.get())
            y = float(self.y_input.get())
        except ValueError:
            return None

        if self.z_input is None:
            return [x, y, self.mode_var.get()]

        try:
            z = float(self.z_input.get())
        except ValueError:
            return None
        return [x, y, z, self.mode_var.get()]
