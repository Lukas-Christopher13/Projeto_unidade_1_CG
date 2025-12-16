from tkinter import *

class RotationInput(Frame):
    def __init__(self, root, command, text=None, **kwargs):
        super().__init__(root, **kwargs)

        Label(self, text="Angulo").pack(side="left")
        
        self.rotation_entry = Entry(self, width=10)
        self.rotation_entry.pack(side="left")

        btn_rotation = Button(self, text="Rotation", command=command)
        btn_rotation.pack(side="left")

    def get(self):
        return float(self.rotation_entry.get())
