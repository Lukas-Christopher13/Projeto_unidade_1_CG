from tkinter import *

from src.components.shared.popup_frame import PopupFrame
from src.utils.matrix_transform import (
    rotation,
    translate,
    scaling,
    reflection_x,
    reflection_y,
    reflection_origin,
    reflection_xy,
    share,
)
from services.log_service import LogService

log = LogService()

WIDTH = 520
HEIGHT = 620



class CombTransformFrame(PopupFrame):
    def __init__(self, root, current_shape, **kwargs):
        super().__init__(root, title="Comb", w=WIDTH, h=HEIGHT, **kwargs)
        self.current_shape = current_shape
        self.queue = []

    def open_popup(self):
        self.sequence_list = Listbox(self.popup, width=60, height=10)
        self.sequence_list.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Rotation
        rotation_frame = Frame(self.popup, bd=2, relief="groove")
        rotation_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=4)
        Label(rotation_frame, text="Rotacao (graus)").grid(row=0, column=0, sticky="w", padx=10)
        self.rotation_entry = Entry(rotation_frame, width=10)
        self.rotation_entry.grid(row=0, column=1, sticky="w")
        Button(rotation_frame, text="Adicionar Rotacao", command=self.add_rotation).grid(
            row=0, column=2, columnspan=2, sticky="w", padx=10
        )

        # Translation
        translation_frame = Frame(self.popup, bd=2, relief="groove")
        translation_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=10, pady=4)
        Label(translation_frame, text="Translate X").grid(
            row=0, column=0, sticky="w", padx=10, pady=4
        )
        self.tx_entry = Entry(translation_frame, width=10)
        self.tx_entry.insert(0, "0.0")
        self.tx_entry.grid(row=0, column=1, sticky="w")

        Label(translation_frame, text="Translate Y").grid(row=0, column=2, sticky="w", padx=10)
        self.ty_entry = Entry(translation_frame, width=10)
        self.ty_entry.insert(0, "0.0")
        self.ty_entry.grid(row=0, column=3, sticky="w")

        Button(translation_frame, text="Adicionar Translate", command=self.add_translation).grid(
            row=1, column=0, columnspan=4, sticky="w", padx=10, pady=(0, 6)
        )

        # Scale
        scale_frame = Frame(self.popup, bd=2, relief="groove")
        scale_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=4)
        Label(scale_frame, text="Scale X").grid(row=0, column=0, sticky="w", padx=10, pady=4)
        self.sx_entry = Entry(scale_frame, width=10)
        self.sx_entry.insert(0, "1.0")
        self.sx_entry.grid(row=0, column=1, sticky="w")

        Label(scale_frame, text="Scale Y").grid(row=0, column=2, sticky="w", padx=10)
        self.sy_entry = Entry(scale_frame, width=10)
        self.sy_entry.insert(0, "1.0")
        self.sy_entry.grid(row=0, column=3, sticky="w")

        Button(scale_frame, text="Adicionar Scale", command=self.add_scale).grid(
            row=1, column=0, columnspan=4, sticky="w", padx=10, pady=(0, 6)
        )

        # Reflection
        reflection_frame = Frame(self.popup, bd=2, relief="groove")
        reflection_frame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=10, pady=4)
        Label(reflection_frame, text="Reflection").grid(
            row=0, column=0, sticky="w", padx=10, pady=4
        )
        self.reflection_var = StringVar(value="x")
        OptionMenu(reflection_frame, self.reflection_var, "x", "y", "origin", "x = y").grid(
            row=0, column=1, sticky="w"
        )
        Button(reflection_frame, text="Adicionar Reflection", command=self.add_reflection).grid(
            row=0, column=2, columnspan=2, sticky="w", padx=10
        )

        # Share (Shear)
        share_frame = Frame(self.popup, bd=2, relief="groove")
        share_frame.grid(row=5, column=0, columnspan=4, sticky="ew", padx=10, pady=4)
        Label(share_frame, text="Share shx").grid(row=0, column=0, sticky="w", padx=10, pady=4)
        self.shx_entry = Entry(share_frame, width=10)
        self.shx_entry.insert(0, "0.0")
        self.shx_entry.grid(row=0, column=1, sticky="w")

        Label(share_frame, text="Share shy").grid(row=0, column=2, sticky="w", padx=10)
        self.shy_entry = Entry(share_frame, width=10)
        self.shy_entry.insert(0, "0.0")
        self.shy_entry.grid(row=0, column=3, sticky="w")

        Button(share_frame, text="Adicionar Share", command=self.add_share).grid(
            row=1, column=0, columnspan=4, sticky="w", padx=10, pady=(0, 6)
        )

        # Actions
        Button(self.popup, text="Transformar", command=self.transform).grid(
            row=6, column=0, padx=10, pady=12, sticky="w"
        )
        Button(self.popup, text="Limpar", command=self.clear_sequence).grid(
            row=6, column=1, padx=10, pady=12, sticky="w"
        )

    def add_rotation(self):
        try:
            angle = float(self.rotation_entry.get())
        except ValueError:
            return

        tx, ty, tz, tw = self.current_shape.second_vertex()
        
        mat = rotation(angle, tx, ty, tz)
        self.queue.append(mat)
        self.sequence_list.insert("end", f"R({angle})")

        log.header("FILA ─ Rotação adicionada")
        log.step(f"Ângulo: θ = {angle}°")
        log.step(f"Centro de rotação: ({tx:.1f}, {ty:.1f}, {tz:.1f})")
        log.matrix("Matriz R composta", mat)

    def add_translation(self):
        try:
            x = float(self.tx_entry.get())
            y = float(self.ty_entry.get())
        except ValueError:
            return

        mat = translate(x, y, 0.0)
        self.queue.append(mat)
        self.sequence_list.insert("end", f"T({x}, {y})")

        log.header("FILA ─ Translação adicionada")
        log.step(f"T(tx={x}, ty={y})")
        log.matrix("Matriz T", mat)

    def add_scale(self):
        try:
            x = float(self.sx_entry.get())
            y = float(self.sy_entry.get())
        except ValueError:
            return
        
        tx, ty, tz, tw = self.current_shape.second_vertex()

        mat = scaling(sx=x, sy=y, tx=tx, ty=ty)
        self.queue.append(mat)
        self.sequence_list.insert("end", f"S({x}, {y})")

        log.header("FILA ─ Escala adicionada")
        log.step(f"Fatores: Sx={x}, Sy={y}")
        log.step(f"Centro de escala: ({tx:.1f}, {ty:.1f})")
        log.matrix("Matriz S composta", mat)

    def add_reflection(self):
        mode = self.reflection_var.get()
        label_map = {"x": "Eixo X", "y": "Eixo Y", "origin": "Origem", "x = y": "Reta y = x"}

        if mode == "x":
            mat = reflection_x()
        elif mode == "y":
            mat = reflection_y()
        elif mode == "origin":
            mat = reflection_origin()
        elif mode == "x = y":
            mat = reflection_xy()
        else:
            return

        self.queue.append(mat)
        self.sequence_list.insert("end", f"R{mode}")

        log.header("FILA ─ Reflexão adicionada")
        log.step(f"Tipo: {label_map.get(mode, mode)}")
        log.matrix("Matriz de Reflexão", mat)

    def add_share(self):
        try:
            shx = float(self.shx_entry.get())
            shy = float(self.shy_entry.get())
        except ValueError:
            return
        
        tx, ty, tz, tw = self.current_shape.second_vertex()

        mat = share(shx=shx, shy=shy, tx=tx, ty=ty)
        self.queue.append(mat)
        self.sequence_list.insert("end", f"Sh({shx}, {shy})")

        log.header("FILA ─ Cisalhamento adicionado")
        log.step(f"shx={shx}, shy={shy}")
        log.step(f"Centro: ({tx:.1f}, {ty:.1f})")
        log.matrix("Matriz Sh composta", mat)


    def transform(self):
        if not self.queue:
            return
        
        m_result = None
        for m in reversed(self.queue):
            if m_result is None:
                m_result = m
            else:
                m_result = m_result @ m

        print(m_result)
        self.current_shape.transform([m_result])

        log.info("Vértices depois:")
        for i, v in enumerate(vertex):
            log.info(f"  V{i}: ({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f})")
        log.separator()

    def clear_sequence(self):
        self.queue = []
        self.sequence_list.delete(0, "end")

    def get_input(self):
        self.popup.destroy()
