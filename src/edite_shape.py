from tkinter import *

from src.utils.windowtk import WindowTk

class EditShape(Frame):
    def __init__(self, root, gl_window: WindowTk, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = gl_window
    
        frame = Frame(root, height=100)
        frame.pack(side=BOTTOM, fill=BOTH, padx=0, pady=0)

        btn_delete = Button(frame, text="delete", command=self.delete)
        btn_delete.pack(pady=5)

        btn_change_color = Button(frame, text="translate", command=self.translate)
        btn_change_color.pack(pady=5)

        btn_to_origin = Button(frame, text="to origin", command=self.to_origin)
        btn_to_origin.pack(pady=5)

    def translate(self):
        shape = self.gl_window.get_selected()
        shape.translate(0.2, 0.2)

    def to_origin(self):
        shape = self.gl_window.get_selected()
        first_point = shape.vertex[0]
        shape.translate(-first_point[0], -first_point[1], -first_point[2])

    def delete(self):
        self.gl_window.delete_shape()

    def change_color(self):
        pass
    
    def test():
        pass
