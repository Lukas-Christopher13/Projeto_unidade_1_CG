
from src.utils.matrix_transform import *
from src.models.gl_window_model import gl_window_model
from components.transform_frame import TransformFrame

class EditShapeController:
    def __init__(self, view, model):
        self.model = model
        self.view = view

        self.view.set_controller(self)

    #adicionar um model para isso!   
    def rotate(self):
        angle, axis = self.view.rotation_input_frame.get()
        shape = gl_window_model.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        if axis == "x":
            rotation = roation_x_axis(angle)
        elif axis == "y":
            rotation = roation_y_axis(angle)
        else:
            rotation = basic_rotation(angle)

        translate_to_center = translate(-xm, -ym, -zm)
        translate_to_inital_position = translate(xm, ym, zm)

        shape.transform([
            translate_to_center,
            rotation,
            translate_to_inital_position
        ])

    def translate(self):
        x, y, z = self.view.translate_input_frame.get()
        shape = gl_window_model.get_selected()
        
        translate_ = translate(x, y, z)
        shape.transform([translate_])

    def scale(self):
        x, y = self.view.scaling_input_frame.get()
        shape = gl_window_model.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        translate_to_center = translate(-xm, -ym, -zm)
        scaling = basic_scaling(x, y) 
        translate_to_inital_position = translate(xm, ym, zm)

        shape.transform([
            translate_to_center,
            scaling,
            translate_to_inital_position
        ])

    def reflection(self, reflection_type):
        if reflection_type == "x":
            reflection_m = reflection_x()
        elif reflection_type == "y":
            reflection_m = reflection_y()
        elif reflection_type == "origin":
            reflection_m = reflection_origin()
        elif reflection_type == "x = y":
            reflection_m = reflection_xy()
        else:
            return

        shape = gl_window_model.get_selected()
        shape.transform([reflection_m])

    def share(self):
        shape = gl_window_model.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex()

        shx, shy, mode = self.view.share_input_frame.get()

        if mode == "x":
            share_m = share(shx=shx)
        elif mode == "y":
            share_m = share(shy=shy)
        else:
            share_m = share(shx=shx, shy=shy)

        translate_to_center = translate(-xm, -ym, -zm)
        translate_to_inital_position = translate(xm, ym, zm)

        shape.transform([
            translate_to_center,
            share_m,
            translate_to_inital_position
        ])

    def transform(self):
        transform_frame = TransformFrame(self.view, gl_window_model.get_selected())
        transform_frame.open_popup()

    def to_origin(self):
        shape = gl_window_model.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex() #melhorar esse nome

        to_center = translate(-xm, -ym, -zm)
        shape.transform([to_center])

    def delete(self):
        gl_window_model.delete_shape()
