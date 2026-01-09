from tkinter import *

from src.views.inputs.abs_input_frame import ABSInputFrame

class RotationInputFrame(ABSInputFrame):
    def _form_content(self):
        Label(self.content, text="Angulo").grid(row=0, column=0)
        
        self.rotation_entry = Entry(self.content, width=10)
        self.rotation_entry.grid(row=0, column=1)

        btn_rotation = Button(self.content, text="Rotation", command=self.command)
        btn_rotation.grid(row=1, column=1)

    def get(self):
        return float(self.rotation_entry.get())
