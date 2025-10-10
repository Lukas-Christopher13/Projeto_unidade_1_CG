import numpy as np
from utils.matrix_transform import translate, scaling, aplay_transformation, basic_scaling

class ViewPort:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def set_coordinate_space(self, u_min, v_min, u_max, v_max):
        self.u_min = u_min
        self.v_min = v_min
        self.u_max = u_max
        self.v_max = v_max

    def transform(self, obj):
        sx = (self.u_max - self.u_min) / (self.x_max - self.x_min)
        sy = (self.v_max - self.v_min) / (self.y_max - self.y_min)

        x_mean, y_mean, z_mean, w_mean = obj.mean(axis=0)
        obj = obj @ translate(-x_mean, -y_mean, -z_mean).T
        obj = obj @ basic_scaling(sx, sy).T
        obj = obj @ translate(self.u_min, self.v_min).T

        print(obj)
        return obj


