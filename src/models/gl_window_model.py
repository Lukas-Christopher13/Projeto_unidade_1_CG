from tkinter import Frame
from typing import List
from src.models.shape import Shape
from src.services.render_service import RenderService
from src.utils.backgrounds import axies_2d, axies_3d


class GlWindowModel:
    window_mode = "2d"
    listeners = []
    shapes: List[Shape] = []
    backgrounds: List[Shape] = []
    frames: List[Frame] = []

    def __init__(self):
        self.to_2d()
    
    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
        RenderService.request_render()
        self.notify()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def add_frame(self, frame: Frame):
        self.frames.append(frame)
    
    def add_background(self, background: Shape):
        self.backgrounds.append(background)

    def rebuild_frames(self):
        for frame in self.frames:
            frame.rebuild()

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

    def use_2d_axies(self):
        self.backgrounds.append(axies_2d)

    def use_3d_axies(self):
        self.backgrounds.append(axies_3d)

    def is_2d(self):
        if self.window_mode == "2d":
            return True
        else:
            return False

    def to_2d(self):
        self.window_mode = "2d"
        self.empty_window()
        self.rebuild_frames()

        self.use_2d_axies()
        
    def to_3d(self):   
        self.window_mode = "3d"
        self.empty_window()   
        self.rebuild_frames()

        #temporariamente vai ficar aqui 
        self.use_3d_axies()

gl_window_model = GlWindowModel()