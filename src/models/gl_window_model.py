from typing import List
from src.models.shape import Shape
from src.utils.backgrounds import axies_3d

from src.utils.shape_factory_3d import ShapeFactory3D

class GlWindowModel:
    window_mode = "2d"
    listeners = []
    shapes: List[Shape] = []
    backgrounds: List[Shape] = []
    
    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
        self.notify()

    def add_listener(self, listener):
        self.listeners.append(listener)
    
    def add_background(self, background: Shape):
        self.backgrounds.append(background)

    def delete_shape(self):
        shape = self.shapes[self.selected]
        shape.clear()

        self.shapes.remove(shape)
        self.notify()

    #delete e remover da lista
    def clear_all(self):
        for shape in self.shapes:
            shape.clear() 

    def notify(self):
        for listener in self.listeners:
            listener.update()

    def set_selected(self, selected: int):
        self.selected = selected

    def get_selected(self):
        return self.shapes[self.selected]
    
    def get_window_mode(self):
        return self.window_mode
    
    def render_shapes(self):
        for shape in self.shapes:
            shape.render()
            
    def empty_window(self):
        self.shapes = []
        self.backgrounds = []
        self.notify()

    def use_3d_axies(self):
        self.backgrounds.append(axies_3d)

    def to_2d(self):
        self.empty_window()
        self.window_mode = "2d"
    
    def to_3d(self):
        self.empty_window()        
        self.window_mode = "3d"

        #temporariamente vai ficar aqui 
        self.use_3d_axies()
        self.add_shape(ShapeFactory3D.cube())

gl_window_model = GlWindowModel()