from tkinter import *

from src.utils.windowtk import WindowTk

from src.components.translate_frame import TranslateFrame

class EditShape(Frame):
    def __init__(self, root, gl_window: WindowTk, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = gl_window

        frame = Frame(root, height=100)
        frame.pack(side=TOP, fill=BOTH, padx=0, pady=0)

        self.translate_frame = TranslateFrame(frame, command=self.translate)

        #Rotation
        # Label(frame, text="Angulo").pack(side=LEFT)
        # rotation_frame = Frame(frame, height=100)
        # frame.pack(side=TOP, fill=BOTH, padx=0, pady=0)


        # self.rotation_input = Entry(frame, width=10)
        # self.rotation_input.grid(row=5, column=1, padx=5, pady=2)

        # btn_rotation = Button(frame, text="Rotation", command=self.rotation)
        # btn_rotation.grid(row=5, column=2, padx=5, pady=2)

        # Linha do botão "To Origin"
        #btn_to_origin = Button(frame, text="To Origin", command=self.to_origin)
        #btn_to_origin.grid(row=6, column=0, columnspan=3, pady=10)

    def translate(self):
        data = self.translate_frame.get_input()
        shape = self.gl_window.get_selected()
        shape.translate(
            x=data[0],
            y=data[1],
            z=data[2]
        )

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
