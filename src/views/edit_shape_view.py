from tkinter import *

from src.views.inputs.scale_input_frame import ScaleInputFrame
from src.views.inputs.rotation_input_frame import RotationInputFrame
from src.views.inputs.translation_input_frame import TranslationInputFrame


class EditShapeView(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        #adicionar os comandos
        self.translate_input_frame = TranslationInputFrame(self, command=self.translate)
        self.translate_input_frame.grid(row=1, column=0)

        self.rotation_input_frame = RotationInputFrame(self, command=self.rotate)
        self.rotation_input_frame.grid(row=2, column=0)

        self.scaling_input_frame = ScaleInputFrame(self, command=self.scale)
        self.scaling_input_frame.grid(row=3, column=0)

        #talvez separar isso
        btn_transform = Button(self, text="Transform", command=self.do_not)
        btn_transform.grid(row=4, column=0)
        
        btn_to_origin = Button(self, text="To Origin", command=self.do_not)
        btn_to_origin.grid(row=5, column=0)

        btn_delete = Button(self, text="Delete", command=self.do_not)
        btn_delete.grid(row=6, column=0)

    def set_controller(self, controller):
        self.controller = controller

    def rotate(self):
        self.controller.rotate()

    def translate(self):
        self.controller.translate()

    def scale(self):
        self.controller.scale()

    def do_not(self):
        pass

