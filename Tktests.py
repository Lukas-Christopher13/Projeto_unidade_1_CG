import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

import tkinter as tk
from tkinter import ttk


class ShearView(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Shear (Cisalhamento)", padding=10, **kwargs)

        # Variáveis
        self.shx_var = tk.StringVar(value="0.0")
        self.shy_var = tk.StringVar(value="0.0")
        self.mode_var = tk.StringVar(value="xy")

        # Labels
        ttk.Label(self, text="Shx:").grid(row=0, column=0, sticky="w")
        ttk.Label(self, text="Shy:").grid(row=1, column=0, sticky="w")

        # Entradas
        ttk.Entry(self, textvariable=self.shx_var, width=10).grid(row=0, column=1, padx=5)
        ttk.Entry(self, textvariable=self.shy_var, width=10).grid(row=1, column=1, padx=5)

        # Modo
        ttk.Label(self, text="Modo:").grid(row=2, column=0, sticky="w", pady=(8, 0))

        ttk.Radiobutton(self, text="Shear X",   variable=self.mode_var, value="x") \
            .grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(self, text="Shear Y",   variable=self.mode_var, value="y") \
            .grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self, text="Shear X + Y", variable=self.mode_var, value="xy") \
            .grid(row=4, column=1, sticky="w")

        # Botões
        ttk.Button(self, text="Aplicar").grid(
            row=5, column=0, pady=10, sticky="ew"
        )
        ttk.Button(self, text="Reset").grid(
            row=5, column=1, pady=10, sticky="ew"
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

root = tk.Tk()
root.title("Transformações 2D")

shear_view = ShearView(root)
shear_view.pack(padx=10, pady=10)

root.mainloop()
