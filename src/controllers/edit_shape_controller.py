import numpy as np

from src.utils.matrix_transform import *
from src.models.gl_window_model import gl_window_model
from components.transform_frame import TransformFrame
from src.components.comb_transform_frame import CombTransformFrame
from services.log_service import LogService

log = LogService()


class EditShapeController:
    def __init__(self, view, model):
        self.model = model
        self.view = view

        self.view.set_controller(self)

    # ── helpers ──────────────────────────────────────────
    def _log_vertices(self, label, vertex):
        """Loga os vértices no formato compacto."""
        log.info(f"{label}:")
        for i, v in enumerate(vertex):
            log.info(f"  V{i}: ({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f})")

    #adicionar um model para isso!   
    def rotate(self):
        result = self.view.rotation_input_frame.get()
        if result is None:
            return
        angle, axis = result
        shape = gl_window_model.get_selected()
        if shape is None:
            return

        xm, ym, zm, wm = self.get_reference_point(shape)

        log.header("ROTAÇÃO")
        log.step(f"Ângulo: θ = {angle}°")
        log.step(f"Eixo: {axis.upper()}")
        log.step(f"Ponto de referência: ({xm:.1f}, {ym:.1f}, {zm:.1f})")
        log.separator()

        if axis == "x":
            rotation = roation_x_axis(angle)
        elif axis == "y":
            rotation = roation_y_axis(angle)
        else:
            rotation = basic_rotation(angle)

        translate_to_center = translate(-xm, -ym, -zm)
        log.step("Passo 1: Transladar centro → origem")
        log.matrix("T₁ = translate(-xm, -ym, -zm)", translate_to_center)

        rad = np.radians(angle)
        log.step(f"Passo 2: Rotacionar θ={angle}° (rad={rad:.4f}) no eixo {axis.upper()}")
        log.matrix(f"R_{axis.upper()}(θ)", rotation)

        translate_to_inital_position = translate(xm, ym, zm)
        log.step("Passo 3: Transladar origem → posição original")
        log.matrix("T₂ = translate(xm, ym, zm)", translate_to_inital_position)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([
            translate_to_center,
            rotation,
            translate_to_inital_position
        ])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def translate(self):
        result = self.view.translate_input_frame.get()
        if result is None:
            return
        x, y, z = result
        shape = gl_window_model.get_selected()
        if shape is None:
            return

        log.header("TRANSLAÇÃO")
        log.step(f"T(tx={x}, ty={y}, tz={z})")

        translate_ = translate(x, y, z)
        log.matrix("Matriz de Translação T", translate_)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([translate_])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def scale(self):
        result = self.view.scaling_input_frame.get()
        if result is None:
            return
        x, y, z = result
        shape = gl_window_model.get_selected()
        if shape is None:
            return
        
        xm, ym, zm, wm = self.get_reference_point(shape)

        log.header("ESCALA")
        log.step(f"Fatores: Sx={x}, Sy={y}, Sz={z}")
        log.step(f"Ponto de referência: ({xm:.1f}, {ym:.1f}, {zm:.1f})")
        log.separator()

        translate_to_center = translate(-xm, -ym, -zm)
        log.step("Passo 1: Transladar centro → origem")
        log.matrix("T₁ = translate(-xm, -ym, -zm)", translate_to_center)

        scaling = basic_scaling(x, y, z)
        log.step(f"Passo 2: Aplicar escala S({x}, {y}, {z})")
        log.matrix("S(sx, sy, sz)", scaling)

        translate_to_inital_position = translate(xm, ym, zm)
        log.step("Passo 3: Transladar origem → posição original")
        log.matrix("T₂ = translate(xm, ym, zm)", translate_to_inital_position)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([
            translate_to_center,
            scaling,
            translate_to_inital_position
        ])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def reflection(self, reflection_type):
        label_map = {
            "x": "Eixo X", "y": "Eixo Y", "origin": "Origem",
            "x = y": "Reta y = x", "XY": "Plano XY",
            "YZ": "Plano YZ", "XZ": "Plano XZ",
        }

        if reflection_type == "x":
            reflection_m = reflection_x()
        elif reflection_type == "y":
            reflection_m = reflection_y()
        elif reflection_type == "origin":
            reflection_m = reflection_origin()
        elif reflection_type == "x = y":
            reflection_m = reflection_xy()
        elif reflection_type == "XY":
            reflection_m = reflection_3d_xy()
        elif reflection_type == "YZ":
            reflection_m = reflection_3d_yz()
        elif reflection_type == "XZ":
            reflection_m = reflection_3d_xz()
        else:
            return

        shape = gl_window_model.get_selected()
        if shape is None:
            return

        log.header("REFLEXÃO")
        log.step(f"Tipo: {label_map.get(reflection_type, reflection_type)}")
        log.matrix("Matriz de Reflexão", reflection_m)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([reflection_m])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def share(self):
        shape = gl_window_model.get_selected()
        if shape is None:
            return
        xm, ym, zm, wm = self.get_reference_point(shape)

        share_data = self.view.share_input_frame.get()
        if share_data is None:
            return

        log.header("CISALHAMENTO (SHEAR)")

        if gl_window_model.is_2d():
            shx, shy, mode = share_data
            log.step(f"Modo 2D — eixo: {mode}")
            log.step(f"shx={shx}, shy={shy}")

            if mode == "x":
                share_m = basic_share(shx=shx)
                log.step(f"Fórmula: y' = y + shx·x  (shx={shx})")
            elif mode == "y":
                share_m = basic_share(shy=shy)
                log.step(f"Fórmula: x' = x + shy·y  (shy={shy})")
            else:
                share_m = basic_share(shx=shx, shy=shy)
                log.step(f"Fórmula: x' = x + shy·y, y' = y + shx·x")
        else:
            shx, shy, shz, mode = share_data
            log.step(f"Modo 3D — eixo fixo: {mode.upper()}")
            log.step(f"shx={shx}, shy={shy}, shz={shz}")

            if mode == "x":
                share_m = share_x(shy=shy, shz=shz)
                log.step(f"Fórmula: x' = x + shy·y + shz·z")
            elif mode == "y":
                share_m = share_y(shx=shx, shz=shz)
                log.step(f"Fórmula: y' = y + shx·x + shz·z")
            else:
                share_m = share_z(shx=shx, shy=shy)
                log.step(f"Fórmula: z' = z + shx·x + shy·y")

        log.step(f"Ponto de referência: ({xm:.1f}, {ym:.1f}, {zm:.1f})")
        log.separator()

        translate_to_center = translate(-xm, -ym, -zm)
        log.step("Passo 1: Transladar centro → origem")
        log.matrix("T₁ = translate(-xm, -ym, -zm)", translate_to_center)

        log.step("Passo 2: Aplicar cisalhamento")
        log.matrix("Sh", share_m)

        translate_to_inital_position = translate(xm, ym, zm)
        log.step("Passo 3: Transladar origem → posição original")
        log.matrix("T₂ = translate(xm, ym, zm)", translate_to_inital_position)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([
            translate_to_center,
            share_m,
            translate_to_inital_position
        ])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def transform(self):
        shape = gl_window_model.get_selected()
        if shape is None:
            return
        transform_frame = TransformFrame(self.view, shape)
        transform_frame.open_popup()

    def to_origin(self):
        shape = gl_window_model.get_selected()
        if shape is None:
            return
        xm, ym, zm, wm = self.get_reference_point(shape)

        log.header("MOVER PARA ORIGEM")
        log.step(f"Centro atual: ({xm:.1f}, {ym:.1f}, {zm:.1f})")

        to_center = translate(-xm, -ym, -zm)
        log.matrix("T = translate(-xm, -ym, -zm)", to_center)

        self._log_vertices("Vértices antes", shape.vertex)
        shape.transform([to_center])
        self._log_vertices("Vértices depois", shape.vertex)
        log.separator()

    def delete(self):
        gl_window_model.delete_shape()

    def clear_all(self):
        gl_window_model.clear_all()
        gl_window_model.shapes.clear()
        gl_window_model.selected = None
        gl_window_model.notify()

        if gl_window_model.is_2d():
            gl_window_model.backgrounds.clear()
            gl_window_model.use_2d_axies()
        else:
            gl_window_model.backgrounds.clear()
            gl_window_model.use_3d_axies()

        from src.services.render_service import RenderService
        RenderService.request_render()

        log.header("LIMPAR TUDO")
        log.step("Todas as formas foram removidas da tela.")
        log.separator()

    def comb(self):
        shape = gl_window_model.get_selected()
        if shape is None and gl_window_model.shapes:
            gl_window_model.set_selected(0)
            shape = gl_window_model.get_selected()

        if shape is None:
            return

        comb_frame = CombTransformFrame(self.view, shape)
        comb_frame.open_popup()

    def get_reference_point(self, shape):
        if gl_window_model.is_2d():
            return shape.second_vertex()
        else:
            return shape.first_vertex()
