from typing import List
from src.models.shape import Shape
from utils.backgrounds import axies_3d

class GlWindowModel:
    listeners = []
    shapes: List[Shape] = []
    backgrounds: List[Shape] = []
    
    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
        self.notify()

    def use_3d_axies(self):
        self.backgrounds.append(axies_3d)
    
    def add_background(self, background: Shape):
        self.backgrounds.append(background)

    #delete e remover da lista
    def clear_all(self):
        for shape in self.shapes:
            shape.clear() 

    def delete_shape(self):
        shape = self.shapes[self.selected]
        shape.clear()

        self.shapes.remove(shape)
        self.notify()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify(self):
        for listener in self.listeners:
            listener.update()

    def set_selected(self, selected: int):
        self.selected = selected

    def get_selected(self):
        return self.shapes[self.selected]
    
    def render_shapes(self):
        for shape in self.shapes:
            shape.render()
            
    def empty_window(self):
        self.shapes = []
        self.backgrounds = []
        self.notify()

singleton = GlWindowModel()