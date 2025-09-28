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

        btn_change_color = Button(frame, text="change_color", command=self.test)
        btn_change_color.pack(pady=5)

    def delete(self):
        self.gl_window.delete_shape()

    def change_color(self):
        pass
    
    def test():
        pass
