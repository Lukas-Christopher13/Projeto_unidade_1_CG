from tkinter import *

from tkinter import *

from src.views.inputs.abs_input_frame import ABSInputFrame

class ScaleInputFrame(ABSInputFrame):
    def _form_content(self):
        Label(self.content, text="X").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.x_input = Entry(self.content, textvariable=StringVar(value="1.0"), width=10)
        self.x_input.grid(row=1, column=1, padx=5, pady=2)

        Label(self.content, text="Y").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.y_input = Entry(self.content, textvariable=StringVar(value="1.0"), width=10)
        self.y_input.grid(row=2, column=1, padx=5, pady=2)

        btn_translate = Button(self.content, text="Scale", command=self.command)
        btn_translate.grid(row=4, column=1, padx=5, pady=2)

    def get(self):
        x = float(self.x_input.get())
        y = float(self.y_input.get())
    
        return [x, y]
