from tkinter import *
import tkinter as tk
from tkinter import ttk

from src.views.inputs.abs_input_frame import ABSInputFrame

class ShareInputFrame(ABSInputFrame):
    def rebuild(self):
        pass

    def _form_content(self):
       # Variáveis
        self.shx_var = tk.StringVar(value="0.0")
        self.shy_var = tk.StringVar(value="0.0")
        self.mode_var = tk.StringVar(value="x")

        # Labels
        ttk.Label(self.content, text="Shx:").grid(row=0, column=0, sticky="w")
        ttk.Label(self.content, text="Shy:").grid(row=1, column=0, sticky="w")

        # Entradas
        self.x_input = ttk.Entry(self.content, textvariable=self.shx_var, width=10)
        self.x_input.grid(row=0, column=1, padx=5)

        self.y_input = ttk.Entry(self.content, textvariable=self.shy_var, width=10)
        self.y_input.grid(row=1, column=1, padx=5)

        # Modo
        ttk.Label(self.content, text="Modo:").grid(row=2, column=0, sticky="w", pady=(8, 0))

        ttk.Radiobutton(self.content, text="Shear X",   variable=self.mode_var, value="x") \
            .grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Shear Y",   variable=self.mode_var, value="y") \
            .grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Shear X + Y", variable=self.mode_var, value="xy") \
            .grid(row=4, column=1, sticky="w")

        # Botões
        ttk.Button(self.content, command=self.command, text="Aplicar").grid(
            row=5, column=0, pady=10, sticky="ew"
        )
        ttk.Button(self.content, text="Reset").grid(
            row=5, column=1, pady=10, sticky="ew"
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def get(self):
        x = float(self.x_input.get())
        y = float(self.y_input.get())
    
        return [x, y, self.mode_var.get()]
