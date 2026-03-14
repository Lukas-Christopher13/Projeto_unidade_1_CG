from collections import deque
from tkinter import * 

from src.components.shared.popup_frame import PopupFrame
from src.components.input_components.rotation_input import RotationInput
from src.components.input_components.translation_input import TranslationInput
from src.components.input_components.scale_input import ScaleInput

from src.utils.matrix_transform import *
from services.log_service import LogService

log = LogService()

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
        if not self.queue:
            return

        log.header("TRANSFORMAÇÃO COMPOSTA (Popup)")
        log.step(f"Sequência de {len(self.queue)} operação(ões)")
        log.step(f"Descrição: {self.transform_description.get()}")
        log.separator()

        # Mostra cada matriz da fila (em ordem lógica = inversa da aplicação)
        log_stack = self.queue.copy()
        log_stack.reverse()

        for idx, mat in enumerate(log_stack):
            log.step(f"Operação {idx + 1}:")
            log.matrix(f"M{idx + 1}", mat)

        # Calcula e exibe a matriz composta
        composed = log_stack[0]
        for m in log_stack[1:]:
            composed = composed @ m
        log.step("Matriz composta final (M_total):")
        log.matrix("M_total", composed)

        # Vértices antes / depois
        vertex = self.current_shape.vertex
        log.info("Vértices antes:")
        for i, v in enumerate(vertex):
            log.info(f"  V{i}: ({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f})")

        self.current_shape.transform(self.queue)

        log.info("Vértices depois:")
        for i, v in enumerate(vertex):
            log.info(f"  V{i}: ({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f})")
        log.separator()

    def rotation(self):
        radians = self.rotation_input.get()

        mat = basic_rotation(radians)
        self.queue.append(mat)
        self.transform_description.set(f"R({radians}) x " + self.transform_description.get())

        log.header("FILA ─ Rotação adicionada")
        log.step(f"Ângulo: {radians}°")
        log.matrix("R(θ)", mat)

    def translation(self):
        xy = self.translation_input.get()

        mat = translate(xy[0], xy[1])
        self.queue.append(mat)
        self.transform_description.set(f"T({xy[0]}, {xy[1]}) x " + self.transform_description.get())

        log.header("FILA ─ Translação adicionada")
        log.step(f"T(tx={xy[0]}, ty={xy[1]})")
        log.matrix("T", mat)

    def scale(self):
        xy = self.scale_input.get()

        mat = basic_scaling(xy[0], xy[1])
        self.queue.append(mat)
        self.transform_description.set(f"S({xy[0]}, {xy[1]}) x " + self.transform_description.get())

        log.header("FILA ─ Escala adicionada")
        log.step(f"Fatores: Sx={xy[0]}, Sy={xy[1]}")
        log.matrix("S", mat)

    def reflection_axis_x(self):
        mat = reflection_x()
        self.queue.append(mat)
        self.transform_description.set("Rx x " + self.transform_description.get())

        log.header("FILA ─ Reflexão adicionada")
        log.step("Tipo: Eixo X")
        log.matrix("Rx", mat)

    def get_input(self):
        try:
            #self.x1 = float(self.ent_x1.get())
            
            self.popup.destroy()

        except ValueError:
            print("Valores Invalidos")


        
