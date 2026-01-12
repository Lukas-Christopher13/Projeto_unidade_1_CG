from abc import ABC, abstractmethod

from tkinter import *
from tkinter import ttk

class ABSInputFrame(ABC, Frame):
    def __init__(self, root, title, command, **kwargs):
        super().__init__(root, **kwargs)

        self.title = title
        self.command = command
        self.expanded = False
        self.columnconfigure(0, weight=1)

        self.label_button = ttk.Button(
            self,
            text=f"▶ {self.title}",
            command=self.toggle,
            style="Header.TButton"
        )
        self.label_button.grid(row=0, column=0, sticky="ew")

        self.content = Frame(self)
        self.content.columnconfigure(1, weight=1)

        self._form_content()

    def toggle(self):
        if self.expanded:
            self.content.grid_remove()
            self.label_button.config(text=self.label_button.cget("text").replace("▼", "▶"))
        else:
            self.content.grid(row=1, column=0, sticky="ew")
            self.label_button.config(text=self.label_button.cget("text").replace("▶", "▼"))

        self.expanded = not self.expanded

    def clear_content(self):
        self.content = Frame(self)

    @abstractmethod
    def _form_content(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def rebuild(self):
        pass



