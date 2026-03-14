from tkinter import Frame, TclError
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
        self.selected = None
        self.to_2d()
    
    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
        self.notify()

        RenderService.request_render()

    def set_single_shape(self, shape: Shape):
        self.shapes = [shape]
        self.selected = 0
        self.notify()

        RenderService.request_render()

    def add_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def add_frame(self, frame: Frame):
        if frame not in self.frames:
            self.frames.append(frame)

    def remove_frame(self, frame: Frame):
        if frame in self.frames:
            self.frames.remove(frame)
    
    def add_background(self, background: Shape):
        self.backgrounds.append(background)

    def rebuild_frames(self):
        alive_frames = []

        for frame in self.frames:
            try:
                # Skip widgets that were destroyed during UI rebuild cycles.
                if not frame.winfo_exists():
                    continue

                frame.rebuild()
                alive_frames.append(frame)
            except (TclError, AttributeError):
                # Drop stale references from previously destroyed widgets.
                continue

        self.frames = alive_frames

    def delete_shape(self):
        if self.selected is None or self.selected < 0 or self.selected >= len(self.shapes):
            self.selected = None
            return
        shape = self.shapes[self.selected]
        shape.clear()

        self.shapes.remove(shape)
        self.selected = None
        self.notify()

        RenderService.request_render()

    #delete e remover da lista
    def clear_all(self):
        for shape in self.shapes:
            shape.clear() 

    def notify(self):
        alive_listeners = []

        for listener in self.listeners:
            try:
                if not hasattr(listener, "update"):
                    continue

                listener.update()
                alive_listeners.append(listener)
            except (TclError, AttributeError, ReferenceError):
                # Listener became invalid after UI/controller rebuild.
                continue

        self.listeners = alive_listeners

    def set_selected(self, selected: int):
        self.selected = selected

    def get_selected(self):
        if self.selected is None:
            return None
        if self.selected < 0 or self.selected >= len(self.shapes):
            self.selected = None
            return None
        return self.shapes[self.selected]
    
    def get_window_mode(self):
        return self.window_mode
    
    def render_shapes(self):
        for shape in self.shapes:
            shape.render()
            
    def empty_window(self):
        self.shapes = []
        self.backgrounds = []
        self.selected = None
        self.notify()

        RenderService.request_render()

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

        RenderService.request_render()
        
    def to_3d(self):   
        self.window_mode = "3d"
        self.empty_window()   
        self.rebuild_frames()

        self.use_3d_axies()

        RenderService.request_render()

gl_window_model = GlWindowModel()