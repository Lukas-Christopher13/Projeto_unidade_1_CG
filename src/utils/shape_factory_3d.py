import numpy as np

from OpenGL.GL import *

from src.models.shape import Shape

class ShapeFactory3D:
    
    @staticmethod
    def cube():
        cube = np.array([
            [ 0.0,   0.0, 0.0,   1.0],
            [ 150.0, 0.0, 0.0,   1.0],
            [ 0.0,   0.0, 150.0, 1.0],
            [ 150.0, 0.0, 150.0, 1.0],

            [ 0.0,   150.0, 0.0,   1.0],
            [ 150.0, 150.0, 0.0,   1.0],
            [ 0.0,   150.0, 150.0, 1.0],
            [ 150.0, 150.0, 150.0, 1.0],
        ], dtype=np.float32)

        cube_edges = [
            (0, 1), (0, 2), (1, 3), (2, 3),  # face baixa
            (4, 5), (4, 6), (5, 7), (6, 7),  # face alta
            (0, 4), (1, 5), (2, 6), (3, 7)   # conectar as faces
        ]
        
        return Shape(matrix=cube, gl_option=GL_LINES, edge_sequence=cube_edges)
    
    def cube_bug():
        cube = np.array([
            [ 150.0, -150.0, 150.0, 1.0],
            [ 150.0, -150.0, -150.0, 1.0],
            [ -150.0, -150.0, -150.0, 1.0],
            [ -150.0, -150.0, 150.0, 1.0],

            [ 150.0, 150.0, 150.0, 1.0],
            [ 150.0, 150.0, -150.0, 1.0],
            [ -150.0, 150.0, -150.0, 1.0],
            [ -150.0,  150.0, 150.0, 1.0],
        ], dtype=np.float32)

        cube_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # face baixa
            (4, 5), (5, 6), (6, 7), (7, 4),  # face alta
            (0, 4), (1, 5), (2, 6), (3, 7)   # conectar as faces
        ]
        
        return Shape(matrix=cube, gl_option=GL_LINES, edge_sequence=cube_edges)
    
    @staticmethod
    def pyramidy():
        pyramidy = np.array([
            [ 0.0,   0.0,   0.0,   1.0],
            [ 300.0, 0.0,   0.0,   1.0],
            [ 0.0,   0.0,   300.0, 1.0],
            [ 300.0, 0.0,   300.0, 1.0],
            [ 150.0, 300.0, 150.0,  1.0],
        ], dtype=np.float32)

        pyramidy_edges = [
            (0, 1), (0, 2), (1, 3), (2, 3),  # face baixa
            (0, 4), (1, 4), (2, 4), (3, 4), 
        ]
        
        return Shape(matrix=pyramidy, gl_option=GL_LINES, edge_sequence=pyramidy_edges)