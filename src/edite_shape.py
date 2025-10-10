from tkinter import *

from src.utils.windowtk import WindowTk
from src.utils.matrix_transform import *

from src.components.translate_frame import TranslateFrame
from src.components.rotation_frame import RotationFrame
from src.components.scaling_frame import ScalingFrame
from src.viewport import ViewPort

class EditShape(Frame):
    viewport = ViewPort(-0.9, -0.9, 0.9, 0.9) # singleton no arquivo de singletons!

    def __init__(self, root, gl_window: WindowTk, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = gl_window
        self.viewport.set_coordinate_space(0.0, 0.0, 0.5, 0.5)

        frame = Frame(root, height=100)
        frame.pack(side=TOP, fill=BOTH, padx=0, pady=0)
        
        self.window_info = Label(frame, text="")
        self.window_info.pack(side=TOP)

        self.translate_frame = TranslateFrame(frame, command=self.translate)
        self.rotation_frame = RotationFrame(frame, command=self.rotation)
        self.scaling_frame = ScalingFrame(frame, command=self.scaling)
        
        btn_to_origin = Button(frame, text="To Origin", command=self.to_origin)
        btn_to_origin.pack(side=BOTTOM)

        btn_delete = Button(frame, text="Delete", command=self.delete)
        btn_delete.pack(side=BOTTOM)

        frame.bind("<Map>", self.test)

    def translate(self):
        x, y, z = self.translate_frame.get_input()
        shape = self.gl_window.get_selected()
        
        translate_ = translate(x, y, z)
        shape.transform([translate_])

    def rotation(self):
        angle = self.rotation_frame.get_input()
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
        x, y, z = self.scaling_frame.get_input()
        shape = self.gl_window.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        translate_to_center = translate(-xm, -ym, -zm)
        scaling = basic_scaling(x, y, z,) 
        translate_to_inital_position = translate(xm, ym, zm)

        shape.transform([
            translate_to_center,
            scaling,
            translate_to_inital_position
        ])

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
