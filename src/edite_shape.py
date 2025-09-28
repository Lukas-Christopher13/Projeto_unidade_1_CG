from tkinter import *

class EditShape(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        frame = Frame(self.parent, height=100)
        frame.pack(side=BOTTOM, fill=BOTH, padx=0, pady=0)

        btn_delete = Button(frame, text="delete", command=self.delete)
        btn_delete.pack(pady=5)

        btn_change_color = Button(frame, text="change_color", command=self.change_color)
        btn_change_color.pack(pady=5)

    def delete(self):
        pass

    def change_color(self):
        pass
        
   