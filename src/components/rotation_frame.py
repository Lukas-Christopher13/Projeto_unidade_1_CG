from tkinter import *

class RotationFrame(Frame):
    def __init__(self, root, command, **kwargs):
        super().__init__(root, **kwargs)

        frame = Frame(root, height=100)
        frame.pack(side=TOP, fill=BOTH, padx=0, pady=0)

        Label(frame, text="Angulo").grid(row=0)

        self.rotation_entry = Entry(frame, width=10)
        self.rotation_entry.grid(row=0, column=1, padx=5, pady=2)

        btn_rotation = Button(frame, text="Rotation", command=command)
        btn_rotation.grid(row=0, column=2, padx=5, pady=2)

    def get_input(self):
        return float(self.rotation_entry.get())
