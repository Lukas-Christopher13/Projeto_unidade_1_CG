import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk

class CollapsibleForm(ttk.Frame):
    def __init__(self, master, title="Menu", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.expanded = False

        # Permite fill horizontal dentro do próprio frame
        self.columnconfigure(0, weight=1)

        # Botão / título clicável
        self.header = ttk.Button(
            self,
            text=f"▶ {title}",
            command=self.toggle,
            style="Header.TButton"
        )
        self.header.grid(row=0, column=0, sticky="ew")

        # Frame que será expandido/recolhido
        self.content = ttk.Frame(self)
        self.content.columnconfigure(1, weight=1)

        # ----- CONTEÚDO DO FORMULÁRIO -----
        ttk.Label(self.content, text="Nome:") \
            .grid(row=0, column=0, sticky="w", padx=10, pady=2)

        ttk.Entry(self.content) \
            .grid(row=0, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(self.content, text="Email:") \
            .grid(row=1, column=0, sticky="w", padx=10, pady=2)

        ttk.Entry(self.content) \
            .grid(row=1, column=1, sticky="ew", padx=10, pady=2)

        ttk.Button(self.content, text="Salvar") \
            .grid(row=2, column=0, columnspan=2, pady=10)
        # ----------------------------------

    def toggle(self):
        if self.expanded:
            self.content.grid_remove()
            self.header.config(text=self.header.cget("text").replace("▼", "▶"))
        else:
            self.content.grid(row=1, column=0, sticky="ew")
            self.header.config(text=self.header.cget("text").replace("▶", "▼"))

        self.expanded = not self.expanded


# ----------------- APP -----------------
root = tk.Tk()
root.title("Formulário Expansível")
root.geometry("300x250")

root.columnconfigure(0, weight=1)

style = ttk.Style()
style.configure("Header.TButton", font=("Arial", 11, "bold"))

form = CollapsibleForm(root, title="Dados do Usuário")
form.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

root.mainloop()
