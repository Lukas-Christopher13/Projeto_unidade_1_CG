from collections import deque
from tkinter import * 

from src.components.shared.popup_frame import PopupFrame
from src.components.input_components.rotation_input import RotationInput
from src.components.input_components.translation_input import TranslationInput
from src.components.input_components.scale_input import ScaleInput

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

        self.rotation_input = RotationInput(self.popup, self.rotation)
        self.rotation_input.grid(row=2, column=0, columnspan=3, pady=12)

        self.translation_input = TranslationInput(self.popup, self.translation)
        self.translation_input.grid(row=3, column=0, columnspan=3, pady=12)

        self.scale_input = ScaleInput(self.popup, self.scale)
        self.scale_input.grid(row=4, column=0, columnspan=3, pady=12)

        btn_reflection_x = Button(self.popup, text="reflection X", command=self.reflection_axis_x)
        btn_reflection_x.grid(row=5, column=0, columnspan=3, pady=12)

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
        radians = self.rotation_input.get()

        self.queue.append(basic_rotation(radians))
        self.transform_description.set(f"R({radians}) x " + self.transform_description.get())

    def translation(self):
        xy = self.translation_input.get()

        self.queue.append(translate(xy[0], xy[1]))
        self.transform_description.set(f"T({xy[0]}, {xy[1]}) x " + self.transform_description.get())

    def scale(self):
        xy = self.scale_input.get()

        self.queue.append(basic_scaling(xy[0], xy[1]))
        self.transform_description.set(f"S({xy[0]}, {xy[1]}) x " + self.transform_description.get())

    def reflection_axis_x(self):
        self.queue.append(reflection_x())
        self.transform_description.set("Rx x " + self.transform_description.get())

    def get_input(self):
        try:
            #self.x1 = float(self.ent_x1.get())
            
            self.popup.destroy()

        except ValueError:
            print("Valores Invalidos")


        