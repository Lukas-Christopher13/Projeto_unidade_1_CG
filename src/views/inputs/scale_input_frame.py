from tkinter import *

from tkinter import *

from src.models.gl_window_model import gl_window_model
from src.views.inputs.abs_input_frame import ABSInputFrame

class ScaleInputFrame(ABSInputFrame):
    def _form_content(self):
        self.rebuild()

        gl_window_model.add_frame(self)
       
    def rebuild(self):
        self.clear_content()

        if gl_window_model.is_2d():
            self._form_2d()
        else:
            self._form_3d()

        bnt_submit = Button(self.content, text="Scale", command=self.command)
        bnt_submit.grid(row=5, column=1, padx=5, pady=2)

    def _form_2d(self):
        Label(self.content, text="X").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.x_input = Entry(self.content, textvariable=StringVar(value="1.0"), width=10)
        self.x_input.grid(row=0, column=1, padx=5, pady=2)

        Label(self.content, text="Y").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.y_input = Entry(self.content, textvariable=StringVar(value="1.0"), width=10)
        self.y_input.grid(row=2, column=1, padx=5, pady=2)

        self.z_input = None

    def _form_3d(self):
        self._form_2d()

        Label(self.content, text="Z").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.z_input = Entry(self.content, textvariable=StringVar(value="1.0"), width=10)
        self.z_input.grid(row=3, column=1, padx=5, pady=2)

    def get(self):
        try:
            x = float(self.x_input.get())
            y = float(self.y_input.get())
        except ValueError:
            return None
        
        if self.z_input is None:
            return [x, y, 1.0]
        else:
            try:
                z = float(self.z_input.get())
            except ValueError:
                return None
        return [x, y, z]
