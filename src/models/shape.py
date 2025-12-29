import numpy as np

from math import cos, sin, radians

from tkinter import *
from OpenGL.GL import *

class Shape():
    def __init__(self, matrix, gl_option, edge_sequence=None, color_matrix = None):
        if len(matrix[0]) != 4:
            matrix = self.__to_4d_array_matrix(matrix)
        self.vertex = np.array(matrix, dtype=np.float32)
        self.gl_option = gl_option
        self.edge_sequence = edge_sequence
        self.color_matrix = color_matrix
    
    def render(self):
        if self.color_matrix is not None:
            self.color_render()
        else:
            self.default_render()

    def color_render(self):
        glBegin(self.gl_option)
        for v, c in zip (self.vertex, self.color_matrix):
            glColor3fv(c)
            glVertex4fv(v)
        glEnd()

    def default_render(self):
        glColor3f(0,0,1)
        glBegin(self.gl_option)
        for v in self.vertex:
            glVertex4fv(v)
        glEnd()

    def render_3d(self, pipeline_3d):
        points = pipeline_3d.transform(self.vertex)

        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(2)
        glBegin(GL_LINES)
        if  self.has_edge_sequence():
            for a, b in self.edge_sequence:
                glVertex2f(points[a][0], points[a][1])
                glVertex2f(points[b][0], points[b][1])
        else:
            for point in points:
                glVertex2f(point[0], point[1])
        glEnd()

    def update(self, gl_option, np_array):
        self.gl_option = gl_option
        self.vertex = np.vstack([self.vertex, np_array])

    def transform(self, tranformations: list):
        for i in tranformations:
            self.vertex = self.vertex @ i.T
        return self.vertex

    def clear(self):
        self.vertex = np.empty((0, 4), dtype=np.float32)

    def mid_point_vertex(self):
        x_mean, y_mean, z_mean, w_mean = self.vertex.mean(axis=0)
        return [x_mean, y_mean, z_mean, w_mean]
    
    def __to_4d_array_matrix(self, matrix):
        for array in matrix:
            if len(array) == 2:
                array.append(0.0)
                array.append(1.0)
            elif len(array) == 3:
                array.append(1.0)
            else:
                raise Exception("Array de tamanho invalido para a converção!")
        return matrix 
    
    def has_edge_sequence(self):
        if self.edge_sequence is None:
            return False
        else:
            return True
        
    def __str__(self):
        return str(self.vertex.T)

