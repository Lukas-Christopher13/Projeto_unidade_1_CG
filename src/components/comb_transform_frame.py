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
        Label(self.popup, text="Rotacao (graus)").grid(row=1, column=0, sticky="w", padx=10)
        self.rotation_entry = Entry(self.popup, width=10)
        self.rotation_entry.grid(row=1, column=1, sticky="w")
        Button(self.popup, text="Adicionar Rotacao", command=self.add_rotation).grid(
            row=1, column=2, columnspan=2, sticky="w", padx=10
        )

        # Translation
        Label(self.popup, text="Translate X").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.tx_entry = Entry(self.popup, width=10)
        self.tx_entry.insert(0, "0.0")
        self.tx_entry.grid(row=2, column=1, sticky="w")

        Label(self.popup, text="Translate Y").grid(row=2, column=2, sticky="w", padx=10)
        self.ty_entry = Entry(self.popup, width=10)
        self.ty_entry.insert(0, "0.0")
        self.ty_entry.grid(row=2, column=3, sticky="w")

        Button(self.popup, text="Adicionar Translate", command=self.add_translation).grid(
            row=3, column=0, columnspan=4, sticky="w", padx=10
        )

        # Scale
        Label(self.popup, text="Scale X").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.sx_entry = Entry(self.popup, width=10)
        self.sx_entry.insert(0, "1.0")
        self.sx_entry.grid(row=4, column=1, sticky="w")

        Label(self.popup, text="Scale Y").grid(row=4, column=2, sticky="w", padx=10)
        self.sy_entry = Entry(self.popup, width=10)
        self.sy_entry.insert(0, "1.0")
        self.sy_entry.grid(row=4, column=3, sticky="w")

        Button(self.popup, text="Adicionar Scale", command=self.add_scale).grid(
            row=5, column=0, columnspan=4, sticky="w", padx=10
        )

        # Reflection
        Label(self.popup, text="Reflection").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.reflection_var = StringVar(value="x")
        OptionMenu(self.popup, self.reflection_var, "x", "y", "origin", "x = y").grid(
            row=6, column=1, sticky="w"
        )
        Button(self.popup, text="Adicionar Reflection", command=self.add_reflection).grid(
            row=6, column=2, columnspan=2, sticky="w", padx=10
        )

        # Share (Shear)
        Label(self.popup, text="Share shx").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.shx_entry = Entry(self.popup, width=10)
        self.shx_entry.insert(0, "0.0")
        self.shx_entry.grid(row=7, column=1, sticky="w")

        Label(self.popup, text="Share shy").grid(row=7, column=2, sticky="w", padx=10)
        self.shy_entry = Entry(self.popup, width=10)
        self.shy_entry.insert(0, "0.0")
        self.shy_entry.grid(row=7, column=3, sticky="w")

        Button(self.popup, text="Adicionar Share", command=self.add_share).grid(
            row=8, column=0, columnspan=4, sticky="w", padx=10
        )

        # Actions
        Button(self.popup, text="Transformar", command=self.transform).grid(
            row=9, column=0, padx=10, pady=12, sticky="w"
        )
        Button(self.popup, text="Limpar", command=self.clear_sequence).grid(
            row=9, column=1, padx=10, pady=12, sticky="w"
        )

    def add_rotation(self):
        try:
            angle = float(self.rotation_entry.get())
        except ValueError:
            return

        tx, ty, tz, tw = self.current_shape.second_vertex()
        
        self.queue.append(rotation(angle, tx, ty, tz))
        self.sequence_list.insert("end", f"R({angle})")

    def add_translation(self):
        try:
            x = float(self.tx_entry.get())
            y = float(self.ty_entry.get())
        except ValueError:
            return
        self.queue.append(translate(x, y, 0.0))
        self.sequence_list.insert("end", f"T({x}, {y})")

    def add_scale(self):
        try:
            x = float(self.sx_entry.get())
            y = float(self.sy_entry.get())
        except ValueError:
            return
        
        tx, ty, tz, tw = self.current_shape.second_vertex()

        self.queue.append(scaling(sx=x, sy=y, tx=tx, ty=ty))
        self.sequence_list.insert("end", f"S({x}, {y})")

    def add_reflection(self):
        mode = self.reflection_var.get()
        if mode == "x":
            self.queue.append(reflection_x())
            self.sequence_list.insert("end", "Rx")
        elif mode == "y":
            self.queue.append(reflection_y())
            self.sequence_list.insert("end", "Ry")
        elif mode == "origin":
            self.queue.append(reflection_origin())
            self.sequence_list.insert("end", "Rorigin")
        elif mode == "x = y":
            self.queue.append(reflection_xy())
            self.sequence_list.insert("end", "Rxy")

    def add_share(self):
        try:
            shx = float(self.shx_entry.get())
            shy = float(self.shy_entry.get())
        except ValueError:
            return
        
        tx, ty, tz, tw = self.current_shape.second_vertex()

        self.queue.append(share(shx=shx, shy=shy, tx=tx, ty=ty))
        self.sequence_list.insert("end", f"Sh({shx}, {shy})")

    def transform(self):
        if not self.queue:
            return
        self.current_shape.transform(self.queue)

    def clear_sequence(self):
        self.queue = []
        self.sequence_list.delete(0, "end")

    def get_input(self):
        self.popup.destroy()
