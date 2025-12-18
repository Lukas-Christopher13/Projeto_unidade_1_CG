from tkinter import *
from src.utils.matrix_transform import *


from src.views.inputs.rotation_input_frame import RotationInputFrame
from src.views.inputs.translation_input_frame import TranslationInputFrame
from src.views.inputs.scale_input_frame import ScaleInputFrame

from src.controllers.edit_shape_controller import EditShapeController

class EditShape(Frame):
    controller = None

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = root.gl_window
        
        self.window_info = Label(self, text="")
        self.window_info.grid(row=1, column=0)

        self.translate_frame = TranslationInputFrame(self, command=self.controller.translate)
        self.translate_frame.grid(row=2, column=0)

        self.rotation_frame = RotationInputFrame(self, command=self.controller.rotation)
        self.rotation_frame.grid(row=3, column=0)

        self.scaling_frame = ScaleInputFrame(self, command=self.controller.scaling)
        self.scaling_frame.grid(row=4, column=0)

        #talvez separar isso
        btn_transform = Button(self, text="Transform", command=self.controller.transform)
        btn_transform.grid(row=5, column=0)
        
        btn_to_origin = Button(self, text="To Origin", command=self.controller.to_origin)
        btn_to_origin.grid(row=6, column=0)

        btn_delete = Button(self, text="Delete", command=self.controller.delete)
        btn_delete.grid(row=7, column=0)

        self.controller = EditShapeController(
            self.gl_window,
            self.translate_frame,
            self.rotation_frame,
            self.scaling_frame
        )

        self.bind("<Map>", self.test)

    
