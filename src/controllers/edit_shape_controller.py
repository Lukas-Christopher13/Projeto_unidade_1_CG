
from src.utils.matrix_transform import *
from src.models.gl_window_model import singleton
from src.components.transform.transform_frame import TransformFrame

class EditShapeController:
    def __init__(self, view, model):
        self.model = model
        self.view = view

        self.view.set_controller(self)

    #adicionar um model para isso!   
    def rotate(self):
        angle = self.view.rotation_input_frame.get()
        shape = singleton.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        translate_to_center = translate(-xm, -ym, -zm)
        rotation = basic_rotation(angle)
        translate_to_inital_position = translate(xm, ym, zm)

        shape.transform([
            translate_to_center,
            rotation,
            translate_to_inital_position
        ])

    def translate(self):
        x, y = self.view.translate_input_frame.get()
        shape = singleton.get_selected()
        
        translate_ = translate(x, y)
        shape.transform([translate_])

    def scale(self):
        x, y = self.view.scaling_input_frame.get()
        shape = singleton.get_selected()
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
        transform_frame = TransformFrame(self.view, singleton.get_selected())
        transform_frame.open_popup()

    def to_origin(self):
        shape = singleton.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        to_center = translate(-xm, -ym, -zm)
        shape.transform([to_center])

    def delete(self):
        singleton.delete_shape()
