from tkinter import *

from src.utils.windowtk import WindowTk

from src.components.translate_frame import TranslateFrame
from src.components.rotation_frame import RotationFrame

class EditShape(Frame):
    def __init__(self, root, gl_window: WindowTk, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = gl_window

        frame = Frame(root, height=100)
        frame.pack(side=TOP, fill=BOTH, padx=0, pady=0)

        self.translate_frame = TranslateFrame(frame, command=self.translate)
        self.rotation_frame = RotationFrame(frame, command=self.rotation)
        
        #Remover Depois/Mover
        btn_to_origin = Button(frame, text="To Origin", command=self.to_origin)
        btn_to_origin.pack(side=BOTTOM)

        btn_delete = Button(frame, text="Delete", command=self.delete)
        btn_delete.pack(side=BOTTOM)

    def translate(self):
        data = self.translate_frame.get_input()
        shape = self.gl_window.get_selected()
        shape.translate(
            x=data[0],
            y=data[1],
            z=data[2]
        )

    def rotation(self):
        angle = self.rotation_frame.get_input()
        shape = self.gl_window.get_selected()
        first_point = shape.vertex[0]
        shape.translate(-first_point[0], -first_point[1], -first_point[2])
        shape.rotation(angle)
        shape.translate(first_point[0], first_point[1], first_point[2])

    def to_origin(self):
        shape = self.gl_window.get_selected()
        first_point = shape.vertex[0]
        shape.translate(-first_point[0], -first_point[1], -first_point[2])

    def delete(self):
        self.gl_window.delete_shape()

    def test():
        pass
