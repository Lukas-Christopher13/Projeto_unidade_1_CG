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
            [-0.7,  0.4, 0.0, 1.0],
            [-0.7, -0.4, 0.0, 1.0],
            [ 0.7, -0.4, 0.0, 1.0],
            [ 0.7,  0.4, 0.0, 1.0],
        ]
        return Shape(rectangle, GL_TRIANGLE_FAN)


    


