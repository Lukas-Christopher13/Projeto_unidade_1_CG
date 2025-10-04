from tkinter import *

class ScalingFrame(Frame):
    def __init__(self, root, command, **kwargs):
        super().__init__(root, **kwargs)

        Label(root, text="Scaling").pack(side=TOP)

        frame = Frame(root, height=100)
        frame.pack(side=TOP, fill=BOTH, padx=0, pady=0)

        Label(frame, text="X").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.x_input = Entry(frame, textvariable=StringVar(value="1.0"), width=10)
        self.x_input.grid(row=1, column=1, padx=5, pady=2)

        Label(frame, text="Y").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.y_input = Entry(frame, textvariable=StringVar(value="1.0"), width=10)
        self.y_input.grid(row=2, column=1, padx=5, pady=2)

        Label(frame, text="Z").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.z_input = Entry(frame, textvariable=StringVar(value="1.0"), width=10)
        self.z_input.grid(row=3, column=1, padx=5, pady=2)

        btn_translate = Button(root, text="Scale", command=command)
        btn_translate.pack(side=TOP, padx=0, pady=0)

    def get_input(self):
        x = float(self.x_input.get())
        y = float(self.y_input.get())
        z = float(self.z_input.get())

        return [x, y, z]

