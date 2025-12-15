from collections import deque
from tkinter import * 

from src.components.shared.popup_frame import PopupFrame
from src.utils.matrix_transform import *

WIDHT = 800
HEIGHT = 800

class TransformFrame(PopupFrame):
    def __init__(self, root, current_shpae, **kwargs):
       super().__init__(
        root,
        w=WIDHT,
        h=HEIGHT, 
        **kwargs
    )
       self.queue = []
       self.log_stack = []
       self.current_shape = current_shpae

    def open_popup(self):
        self.transform_description = StringVar()
        self.transform_description.set("M")
    
        label = Label(self.popup, textvariable=self.transform_description, font=("Arial", 14))
        label.grid(row=0, column=0, pady=5)

        btn_rotation = Button(self.popup, text="rotate", command=self.rotation)
        btn_rotation.grid(row=2, column=0, columnspan=3, pady=12)

        btn_translation = Button(self.popup, text="translate", command=self.translation)
        btn_translation.grid(row=3, column=0, columnspan=3, pady=12)

        btn_scale = Button(self.popup, text="scale", command=self.scale)
        btn_scale.grid(row=4, column=0, columnspan=3, pady=12)

        btn_transform = Button(self.popup, text="Transform", command=self.transform)
        btn_transform.grid(row=0, column=1, columnspan=3, pady=12)

    def transform(self):
        self.print_sequence()
        self.current_shape.transform(self.queue)
        print(self.current_shape.vertex)
    
    def print_sequence(self):
        self.log_stack = self.queue.copy()
        self.log_stack.reverse()
        
        print("---sequencia lógica---")
        for i in self.log_stack:
            print(i)
        
        print("-----------------")
        current = self.log_stack[0]
        for i in range(len(self.log_stack) -1):
            current = current @ self.log_stack[i + 1]
            print(current)

        print(self.current_shape.vertex @ current.T)

    def rotation(self):
        self.queue.append(basic_rotation(30.0))
        self.transform_description.set("R(30) x " + self.transform_description.get())

    def translation(self):
        self.queue.append(translate(400, 400))
        self.transform_description.set("T(400, 400) x " + self.transform_description.get())

    def scale(self):
        self.queue.append(basic_scaling(2,2))
        self.transform_description.set("S(2, 2) x " + self.transform_description.get())

    def get_input(self):
        try:
            #self.x1 = float(self.ent_x1.get())
            
            self.popup.destroy()

        except ValueError:
            print("Valores Invalidos")


        