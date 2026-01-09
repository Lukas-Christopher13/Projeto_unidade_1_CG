from tkinter import *
from tkinter import ttk

from src.views.inputs.abs_input_frame import ABSInputFrame

class TranslationInputFrame(ABSInputFrame):
    def _form_content(self):
        Label(self.content, text="X").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.x_input = Entry(self.content, textvariable=StringVar(value="0.0"), width=10)
        self.x_input.grid(row=0, column=1, padx=5, pady=2)

        Label(self.content, text="Y").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.y_input = Entry(self.content, textvariable=StringVar(value="0.0"), width=10)
        self.y_input.grid(row=2, column=1, padx=5, pady=2)

        bnt_submit = Button(self.content, text="Translate", command=self.command)
        bnt_submit.grid(row=4, column=1, padx=5, pady=2)

    def get(self):
        x = float(self.x_input.get())
        y = float(self.y_input.get())
    
        return [x, y]
