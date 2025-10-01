from tkinter import *

from src.utils.windowtk import WindowTk

class EditShape(Frame):
    def __init__(self, root, gl_window: WindowTk, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = gl_window
    
        frame = Frame(root, height=100)
        frame.pack(side=BOTTOM, fill=BOTH, padx=0, pady=0)

        #Translate
        Label(frame, text="Translate").grid(row=0, column=0, columnspan=2, pady=5)

        Label(frame, text="X").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.x_input = Entry(frame, width=10)
        self.x_input.grid(row=1, column=1, padx=5, pady=2)

        Label(frame, text="Y").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.y_input = Entry(frame, width=10)
        self.y_input.grid(row=2, column=1, padx=5, pady=2)

        Label(frame, text="Z").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.z_input = Entry(frame, width=10)
        self.z_input.grid(row=3, column=1, padx=5, pady=2)

        btn_translate = Button(frame, text="Translate", command=self.translate)
        btn_translate.grid(row=4, column=0, columnspan=2, pady=10)

        #Rotation
        Label(frame, text="Angulo:").grid(row=5, column=0, sticky="e", padx=5, pady=2)

        self.rotation_input = Entry(frame, width=10)
        self.rotation_input.grid(row=5, column=1, padx=5, pady=2)

        btn_rotation = Button(frame, text="Rotation", command=self.rotation)
        btn_rotation.grid(row=5, column=2, padx=5, pady=2)

        # Linha do botão "To Origin"
        btn_to_origin = Button(frame, text="To Origin", command=self.to_origin)
        btn_to_origin.grid(row=6, column=0, columnspan=3, pady=10)


    def translate(self):
        x = float(self.x_input.get())
        y = float(self.y_input.get())
        z = float(self.z_input.get())

        shape = self.gl_window.get_selected()
        shape.translate(x, y, z)

    def to_origin(self):
        shape = self.gl_window.get_selected()
        first_point = shape.vertex[0]
        shape.translate(-first_point[0], -first_point[1], -first_point[2])

    #mover para o centro faz o objeto rotacionar me torno de si!
    def rotation(self):
        angle = float(self.rotation_input.get())

        shape = self.gl_window.get_selected()
        first_point = shape.vertex[0]
        shape.translate(-first_point[0], -first_point[1], -first_point[2])
        shape.rotation(angle)
        shape.translate(first_point[0], first_point[1], first_point[2])

    def delete(self):
        self.gl_window.delete_shape()

    def change_color(self):
        pass
    
    def test():
        pass
