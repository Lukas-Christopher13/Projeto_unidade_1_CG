from tkinter import *

from src.views.inputs.abs_input_frame import ABSInputFrame

class ReflectionInputFrame(ABSInputFrame):

    def rebuild(self):
        pass

    def _form_content(self):
        btn_x_reflection = Button(self.content, text="X", command=lambda: self.command("x"))
        btn_x_reflection.grid(row=0, column=0)
        
        btn_y_reflection = Button(self.content, text="Y", command=lambda: self.command("y"))
        btn_y_reflection.grid(row=0, column=1)

        btn_origin_reflection = Button(self.content, text="origin", command=lambda: self.command("origin"))
        btn_origin_reflection.grid(row=1, column=0)

        btn_xy_reflection = Button(self.content, text="X = Y", command=lambda: self.command("x = y"))
        btn_xy_reflection.grid(row=1, column=1)
    
    def get(self):
        pass
