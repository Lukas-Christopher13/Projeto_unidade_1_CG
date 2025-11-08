from OpenGL.GL import *

from src.utils.shape import Shape

class ShapeFactory:
    @staticmethod
    def triangle():
        triangle = [
            [ 0.0,  300.0, 0.0, 1.0],
            [-300.0, -300.0, 0.0, 1.0],
            [ 300.0, -300.0, 0.0, 1.0],
        ]
        return Shape(triangle, GL_TRIANGLE_FAN)
    
    @staticmethod
    def square():
        square = [
            [-300.0,  300.0, 0.0, 1.0],
            [-300.0, -300.0, 0.0, 1.0],
            [ 300.0, -300.0, 0.0, 1.0],
            [ 300.0,  300.0, 0.0, 1.0],
        ]
        return Shape(square, GL_TRIANGLE_FAN)
    
    @staticmethod
    def rectangle():
        rectangle = [
            [-700.0,  400.0, 0.0, 1.0],
            [-700.0, -400.0, 0.0, 1.0],
            [ 700.0, -400.0, 0.0, 1.0],
            [ 700.0,  400.0, 0.0, 1.0],
        ]
        return Shape(rectangle, GL_TRIANGLE_FAN)
    
    def line():
        line = [
            [0.0,  0.0, 0.0, 1.0],
            [500.0,  500.0, 0.0, 1.0]
        ]
        return Shape(line, GL_LINES)


