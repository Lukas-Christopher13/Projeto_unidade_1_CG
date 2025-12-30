import numpy as np

from tkinter import *
from OpenGL.GL import *

DEFAULT_COLOR = [0.0, 0.0, 1.0]


class Shape():
    def __init__(self, matrix, gl_option, edge_sequence=None):
        self.vertex = self.__to_4_columns(matrix)
        self.gl_option = gl_option
        self.edge_sequence = edge_sequence

    def __to_4_columns(self, matrix):
        matriz = np.array(matrix, dtype=np.float32)
        cols = matriz.shape[1]

        if cols >= 4:
            return matriz

        faltam = 4 - cols
        extra = np.zeros((matriz.shape[0], faltam), dtype=matriz.dtype)

        # última coluna = 1
        extra[:, -1] = 1

        return np.hstack((matriz, extra))
    
    def render(self):
        glBegin(self.gl_option)
        for v in self.vertex:
            self.draw_point(v)
        glEnd()

    def draw_point(self, v):
        if self.has_color():
            glColor3fv(v[4:7])
        else:
            glColor3fv(DEFAULT_COLOR)
        glVertex4fv(v[0:4])

    def render_3d(self, pipeline_3d):
        points = pipeline_3d.transform(self.vertex)

        glLineWidth(2)
        glBegin(GL_LINES)
        if  self.has_edge_sequence():
            for a, b in self.edge_sequence:
                self.apply_color(points[a])
                glVertex2f(points[a][0], points[a][1])

                self.apply_color(points[b])
                glVertex2f(points[b][0], points[b][1])
        else:
            for point in points:
                self.apply_color(point)
                glVertex2f(point[0], point[1])
        glEnd()

    def update(self, gl_option, np_array):
        self.gl_option = gl_option
        self.vertex = np.vstack([self.vertex, np_array])

    def transform(self, tranformations: list):
        for M in tranformations:
            self.apply_transform(M)
        return self.vertex
    
    def apply_transform(self, M):
        for v in self.vertex:
            pos = v[0:4]
            v[0:4] = M @ pos  

    def clear(self):
        self.vertex = np.empty((0, 4), dtype=np.float32)

    def mid_point_vertex(self):
        x_mean, y_mean, z_mean, w_mean = self.vertex[:, :4].mean(axis=0)
        return [x_mean, y_mean, z_mean, w_mean]
     
    def has_edge_sequence(self):
        if self.edge_sequence is None:
            return False
        else:
            return True
        
    def apply_color(self, v):
        if self.has_color():
            glColor3fv(v[4:7])
        else:
            glColor3fv(DEFAULT_COLOR)

    def has_color(self):
        if self.vertex.shape[1] > 4:
            return True
        else:
            return False
        
    def __str__(self):
        return str(self.vertex.T)

