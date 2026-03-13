from tkinter import *

from src.models.gl_window_model import gl_window_model
from src.views.inputs.abs_input_frame import ABSInputFrame

class ReflectionInputFrame(ABSInputFrame):
    def _form_content(self):
        self.rebuild()

        gl_window_model.add_frame(self)

    def rebuild(self):
        self.clear_content()

        if gl_window_model.is_2d():
            self._form_2d()
        else:
            self._form_3d()

    def _form_2d(self):
        btn_x_reflection = Button(self.content, text="X", command=lambda: self.command("x"))
        btn_x_reflection.grid(row=0, column=0)
        
        btn_y_reflection = Button(self.content, text="Y", command=lambda: self.command("y"))
        btn_y_reflection.grid(row=0, column=1)

        btn_origin_reflection = Button(self.content, text="origin", command=lambda: self.command("origin"))
        btn_origin_reflection.grid(row=1, column=0)

        btn_xy_reflection = Button(self.content, text="X = Y", command=lambda: self.command("x = y"))
        btn_xy_reflection.grid(row=1, column=1)

    def _form_3d(self):
        btn_x_reflection = Button(self.content, text="XY", command=lambda: self.command("XY"))
        btn_x_reflection.grid(row=0, column=0)
        
        btn_y_reflection = Button(self.content, text="YZ", command=lambda: self.command("YZ"))
        btn_y_reflection.grid(row=0, column=1)

        btn_z_reflection = Button(self.content, text="XZ", command=lambda: self.command("XZ"))
        btn_z_reflection.grid(row=0, column=2)
    
    def get(self):
        pass
