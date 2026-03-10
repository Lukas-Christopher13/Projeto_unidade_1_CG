import numpy as np

from tkinter import *

from src.utils.windowtk import WindowTk
from src.utils.matrix_transform import *

from src.components.translate_frame import TranslateFrame
from src.components.rotation_frame import RotationFrame
from src.components.scaling_frame import ScalingFrame

from services.log_service import LogService

log = LogService()


class EditShape(Frame):

    def __init__(self, root, gl_window: WindowTk, **kwargs):
        super().__init__(root, **kwargs)
        self.gl_window = gl_window

        frame = Frame(root, height=100)
        frame.pack(side=TOP, fill=BOTH, padx=0, pady=0)
        
        self.window_info = Label(frame, text="")
        self.window_info.pack(side=TOP)

        self.translate_frame = TranslateFrame(frame, command=self.translate)
        self.rotation_frame = RotationFrame(frame, command=self.rotation)
        self.scaling_frame = ScalingFrame(frame, command=self.scaling)
        
        btn_to_origin = Button(frame, text="To Origin", command=self.to_origin)
        btn_to_origin.pack(side=BOTTOM)

        btn_delete = Button(frame, text="Delete", command=self.delete)
        btn_delete.pack(side=BOTTOM)

        frame.bind("<Map>", self.test)

    def _log_vertices(self, label, vertex):
        """Loga os vértices no formato compacto."""
        log.info(f"{label}:")
        count = len(vertex)
        show = min(count, 6)
        for i in range(show):
            v = vertex[i]
            log.info(f"  V{i}: ({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f})")
        if count > 6:
            log.info(f"  ... (+{count - 6} vértices)")

    def translate(self):
        x, y, z = self.translate_frame.get_input()
        shape = self.gl_window.get_selected()

        log.header("TRANSLAÇÃO")
        log.step(f"T(tx={x}, ty={y}, tz={z})")

        translate_ = translate(x, y, z)
        log.matrix("Matriz de Translação T", translate_)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([translate_])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def rotation(self):
        angle = self.rotation_frame.get_input()
        shape = self.gl_window.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex()

        log.header("ROTAÇÃO")
        log.step(f"Ângulo: θ = {angle}°")
        log.step(f"Centro da forma: ({xm:.1f}, {ym:.1f}, {zm:.1f})")
        log.separator()

        translate_to_center = translate(-xm, -ym, -zm)
        log.step("Passo 1: Transladar centro → origem")
        log.matrix("T₁ = translate(-xm, -ym, -zm)", translate_to_center)

        rotation = basic_rotation(angle)
        rad = np.radians(angle)
        log.step(f"Passo 2: Rotacionar θ={angle}° (rad={rad:.4f})")
        log.matrix("R(θ)", rotation)

        translate_to_inital_position = translate(xm, ym, zm)
        log.step("Passo 3: Transladar origem → centro original")
        log.matrix("T₂ = translate(xm, ym, zm)", translate_to_inital_position)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([
            translate_to_center,
            rotation,
            translate_to_inital_position
        ])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def scaling(self):
        x, y, z = self.scaling_frame.get_input()
        shape = self.gl_window.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex()

        log.header("ESCALA")
        log.step(f"Fatores: Sx={x}, Sy={y}, Sz={z}")
        log.step(f"Centro da forma: ({xm:.1f}, {ym:.1f}, {zm:.1f})")
        log.separator()

        translate_to_center = translate(-xm, -ym, -zm)
        log.step("Passo 1: Transladar centro → origem")
        log.matrix("T₁ = translate(-xm, -ym, -zm)", translate_to_center)

        scaling_mat = basic_scaling(x, y, z)
        log.step(f"Passo 2: Aplicar escala S({x}, {y}, {z})")
        log.matrix("S(sx, sy, sz)", scaling_mat)

        translate_to_inital_position = translate(xm, ym, zm)
        log.step("Passo 3: Transladar origem → centro original")
        log.matrix("T₂ = translate(xm, ym, zm)", translate_to_inital_position)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([
            translate_to_center,
            scaling_mat,
            translate_to_inital_position
        ])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def to_origin(self):
        shape = self.gl_window.get_selected()
        xm, ym, zm, wm = shape.mid_point_vertex()

        log.header("MOVER PARA ORIGEM")
        log.step(f"Centro atual: ({xm:.1f}, {ym:.1f}, {zm:.1f})")

        to_center = translate(-xm, -ym, -zm)
        log.matrix("T = translate(-xm, -ym, -zm)", to_center)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([to_center])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def delete(self):
        self.gl_window.delete_shape()

    def test(self, event=None):
        width = self.gl_window.winfo_width()
        height = self.gl_window.winfo_height()
        self.window_info.config(text=f"Window Size: {width} X {height}")
