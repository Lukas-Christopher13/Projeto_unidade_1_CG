import numpy as np

from OpenGL.GL import *

from src.models.shape import Shape

class ShapeFactory3D:
    
    @staticmethod
    def cube():
        cube = np.array([
            [ 25.0, -25.0, 25.0, 1.0],
            [ 25.0, -25.0, -25.0, 1.0],
            [ -25.0, -25.0, -25.0, 1.0],
            [ -25.0, -25.0, 25.0, 1.0],

            [ 25.0, 25.0, 25.0, 1.0],
            [ 25.0, 25.0, -25.0, 1.0],
            [ -25.0, 25.0, -25.0, 1.0],
            [ -25.0,  25.0, 25.0, 1.0],
        ], dtype=np.float32)

        cube_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # face baixa
            (4, 5), (5, 6), (6, 7), (7, 4),  # face alta
            (0, 4), (1, 5), (2, 6), (3, 7)   # conectar as faces
        ]
        
        return Shape(matrix=cube, gl_option=GL_LINES, edge_sequence=cube_edges)