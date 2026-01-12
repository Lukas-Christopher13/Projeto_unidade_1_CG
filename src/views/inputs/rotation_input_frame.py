import tkinter as tk

from tkinter import *
from tkinter import ttk

from src.models.gl_window_model import gl_window_model
from src.views.inputs.abs_input_frame import ABSInputFrame

class RotationInputFrame(ABSInputFrame):
    axis = None

    def _form_content(self):
        self.rebuild()

        gl_window_model.add_frame(self)
 
    def rebuild(self):
        self.clear_content()

        if gl_window_model.is_2d():
            self._form_2d()
        else:
            self._form_3d()

        btn_rotation = Button(self.content, text="Rotation", command=self.command)
        btn_rotation.grid(row=5, column=1)

    def _form_2d(self):
        Label(self.content, text="Angulo").grid(row=0, column=0)
        
        self.rotation_entry = Entry(self.content, width=10)
        self.rotation_entry.grid(row=0, column=1)

    def _form_3d(self):
        self.axis = tk.StringVar(value="z")

        self._form_2d()
       
        ttk.Radiobutton(self.content, text="X axis",  variable=self.axis, value="x") \
            .grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Y axis",  variable=self.axis, value="y") \
            .grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self.content, text="Z axis", variable=self.axis, value="z") \
            .grid(row=4, column=1, sticky="w")

    def get(self):
        angle = float(self.rotation_entry.get())

        if self.axis is None:
            return [angle, "z"]
        else:
            return [angle, self.axis.get()]