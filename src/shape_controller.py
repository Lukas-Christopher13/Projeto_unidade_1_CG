from tkinter import *

from src.utils.windowtk import WindowTk
from src.utils.matrix_transform import *


from src.views.inputs.rotation_input_frame import RotationInputFrame
from src.views.inputs.translation_input_frame import TranslationInputFrame
from src.views.inputs.scale_input_frame import ScaleInputFrame


from components.transform.transform_frame import TransformFrame

class EditShape(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = root.gl_window
        
        self.window_info = Label(self, text="")
        self.window_info.grid(row=1, column=0)

        self.translate_frame = TranslationInputFrame(self, command=self.translate)
        self.translate_frame.grid(row=2, column=0)

        self.rotation_frame = RotationInputFrame(self, command=self.rotation)
        self.rotation_frame.grid(row=3, column=0)

        self.scaling_frame = ScaleInputFrame(self, command=self.scaling)
        self.scaling_frame.grid(row=4, column=0)

        btn_transform = Button(self, text="Transform", command=self.transform)
        btn_transform.grid(row=5, column=0)
        
        btn_to_origin = Button(self, text="To Origin", command=self.to_origin)
        btn_to_origin.grid(row=6, column=0)

        btn_delete = Button(self, text="Delete", command=self.delete)
        btn_delete.grid(row=7, column=0)

        self.bind("<Map>", self.test)

    def translate(self):
        x, y = self.translate_frame.get()
        shape = self.gl_window.get_selected()
        
        translate_ = translate(x, y)
        shape.transform([translate_])

    def rotation(self):
        angle = self.rotation_frame.get()
        shape = self.gl_window.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        translate_to_center = translate(-xm, -ym, -zm)
        rotation = basic_rotation(angle)
        translate_to_inital_position = translate(xm, ym, zm)

        shape.transform([
            translate_to_center,
            rotation,
            translate_to_inital_position
        ])

    def scaling(self):
        x, y = self.scaling_frame.get()
        shape = self.gl_window.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        translate_to_center = translate(-xm, -ym, -zm)
        scaling = basic_scaling(x, y) 
        translate_to_inital_position = translate(xm, ym, zm)

        shape.transform([
            translate_to_center,
            scaling,
            translate_to_inital_position
        ])

    def transform(self):
        transform_frame = TransformFrame(self.gl_window, self.gl_window.get_selected())
        transform_frame.open_popup()

    def to_origin(self):
        shape = self.gl_window.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        to_center = translate(-xm, -ym, -zm)
        shape.transform([to_center])

    def delete(self):
        self.gl_window.delete_shape()

    def test(self, event=None):
        width = self.gl_window.winfo_width()
        height = self.gl_window.winfo_height()
        self.window_info.config(text=f"Window Size: {width} X {height}")
