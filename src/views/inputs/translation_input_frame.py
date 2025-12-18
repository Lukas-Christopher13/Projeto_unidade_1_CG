from tkinter import *

class TranslationInputFrame(Frame):
    def __init__(self, root, command, text=None, **kwargs):
        super().__init__(root, **kwargs)

        Label(root, text="Translate").grid(row=0, column=1, padx=5, pady=2)

        Label(self, text="X").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.x_input = Entry(self, textvariable=StringVar(value="0.0"), width=10)
        self.x_input.grid(row=1, column=1, padx=5, pady=2)

        Label(self, text="Y").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.y_input = Entry(self, textvariable=StringVar(value="0.0"), width=10)
        self.y_input.grid(row=2, column=1, padx=5, pady=2)

        btn_translate = Button(self, text="Translate", command=command)
        btn_translate.grid(row=4, column=1, padx=5, pady=2)

    def get(self):
        x = float(self.x_input.get())
        y = float(self.y_input.get())
    
        return [x, y]


