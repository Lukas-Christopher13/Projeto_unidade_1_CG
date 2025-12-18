
from src.utils.matrix_transform import *
from src.components.transform.transform_frame import TransformFrame

class EditShapeController:
    #dar um jeito de pegar o frame atuals com 
    #gl_window.get_selected

    def __init__(self, gl_window, translate_frame, rotation_frame, scaling_frame):
        self.gl_window = gl_window
        self.translate_frame = translate_frame
        self.rotation_frame = rotation_frame
        self.scaling_frame = scaling_frame

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
