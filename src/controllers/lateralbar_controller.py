from src.models.gl_window_model import gl_window_model
from src.controllers.edit_shape_controller import EditShapeController
from src.models.shape import Shape
from OpenGL.GL import GL_POINTS, GL_LINE_LOOP
from src.services.render_service import RenderService
import numpy as np

class LateralBarController:
    def __init__(self, view, gl_window_controller, model):
        self.view = view
        self.model = model
        self.gl_window_controller = gl_window_controller

        self.edit_shape_controller = EditShapeController(self.view.edit_shape_view, None)

        gl_window_model.add_listener(self)
        self.view.set_point_actions(self.add_point_to_shape)

        self._selected_line_algorithm = None
        self._selected_circle_algorithm = None
        self._editing_shape_index = None

    def _reset_scene_with_axes(self):
        gl_window_model.empty_window()
        gl_window_model.selected = None
        self._editing_shape_index = None
        self.view.set_points([])

        if gl_window_model.is_2d():
            gl_window_model.use_2d_axies()
        else:
            gl_window_model.use_3d_axies()

        RenderService.request_render()

    def update(self):
        if self._editing_shape_index is not None and self._editing_shape_index < len(gl_window_model.shapes):
            shape = gl_window_model.shapes[self._editing_shape_index]
            points = [v[:3] for v in shape.vertex]
            self.view.set_points(points)
            gl_window_model.set_selected(self._editing_shape_index)
            return

        if gl_window_model.selected is None and gl_window_model.shapes:
            gl_window_model.set_selected(len(gl_window_model.shapes) - 1)

        selected = gl_window_model.get_selected()
        if selected is None:
            self.view.set_points([])
            return

        points = [v[:3] for v in selected.vertex]
        self.view.set_points(points)

    def show_transform_screen(self, reset_scene=True):
        if reset_scene:
            self._reset_scene_with_axes()
        else:
            self._editing_shape_index = None
            self.view.set_points([])

        self.view.show_transform_screen()

    def show_line_algorithm_screen(self, name: str, algorithm):
        self._reset_scene_with_axes()
        self._selected_line_algorithm = algorithm
        self.view.show_line_algorithm_screen(name)
        self.view.set_algorithm_action("Desenhar Linha", self._run_line_algorithm)

    def show_circle_algorithm_screen(self, name: str, algorithm):
        self._reset_scene_with_axes()
        self._selected_circle_algorithm = algorithm
        self.view.show_circle_algorithm_screen(name)
        self.view.set_algorithm_action("Desenhar Circulo", self._run_circle_algorithm)

    def _run_line_algorithm(self):
        if self._selected_line_algorithm is None:
            return

        values = self.view.get_line_inputs()
        if values is None:
            return

        points = self._selected_line_algorithm(
            x1=values["x1"],
            y1=values["y1"],
            x2=values["x2"],
            y2=values["y2"],
        )
        gl_window_model.set_single_shape(Shape(points, GL_POINTS))
        self._editing_shape_index = None

    def _run_circle_algorithm(self):
        if self._selected_circle_algorithm is None:
            return

        values = self.view.get_circle_inputs()
        if values is None:
            return

        points = self._selected_circle_algorithm(
            values["radian"],
            values["origin_x"],
            values["origin_y"],
        )
        gl_window_model.set_single_shape(Shape(points, GL_POINTS))
        self._editing_shape_index = None

    def add_point_to_shape(self):
        values = self.view.get_point_input()
        if values is None:
            return

        if self._editing_shape_index is None or self._editing_shape_index >= len(gl_window_model.shapes):
            point = np.array([[values[0], values[1], values[2], 1.0]], dtype=np.float32)
            shape = Shape(point.tolist(), GL_LINE_LOOP)
            self._refresh_closed_edges(shape)
            gl_window_model.set_single_shape(shape)
            self._editing_shape_index = 0
            gl_window_model.set_selected(self._editing_shape_index)
        else:
            shape = gl_window_model.shapes[self._editing_shape_index]
            point = self._build_point_for_shape(shape, values)
            shape.update(GL_LINE_LOOP, point)
            self._refresh_closed_edges(shape)
            RenderService.request_render()

        self.update()

    def _refresh_closed_edges(self, shape):
        total = len(shape.vertex)
        if total < 2:
            shape.edge_sequence = None
            return

        if gl_window_model.is_2d():
            shape.edge_sequence = [(i, (i + 1) % total) for i in range(total)]
            return

        inferred = self._infer_3d_edges(shape.vertex[:, :3])
        if inferred is not None:
            shape.edge_sequence = inferred
        else:
            # Fallback for arbitrary 3D shapes: keep sequential closed contour.
            shape.edge_sequence = [(i, (i + 1) % total) for i in range(total)]

    def _infer_3d_edges(self, points):
        n = len(points)

        # Pyramid: 4-point base + 1 apex.
        if n == 5:
            z_vals = np.round(points[:, 2], 6)
            unique_z, counts = np.unique(z_vals, return_counts=True)
            if len(unique_z) == 2 and sorted(counts.tolist()) == [1, 4]:
                apex_z = unique_z[np.argmin(counts)]
                apex_idx = int(np.where(z_vals == apex_z)[0][0])
                base_idx = [i for i in range(n) if i != apex_idx]

                ordered_base = self._sort_indices_by_xy_angle(points, base_idx)
                edges = []

                for i in range(4):
                    a = ordered_base[i]
                    b = ordered_base[(i + 1) % 4]
                    edges.append((a, b))

                for i in ordered_base:
                    edges.append((apex_idx, i))

                return edges

        # Cube-like prism: 2 layers of 4 points each.
        if n == 8:
            z_vals = np.round(points[:, 2], 6)
            unique_z, counts = np.unique(z_vals, return_counts=True)
            if len(unique_z) == 2 and counts[0] == 4 and counts[1] == 4:
                lower_idx = np.where(z_vals == unique_z[0])[0].tolist()
                upper_idx = np.where(z_vals == unique_z[1])[0].tolist()

                lower_ordered = self._sort_indices_by_xy_angle(points, lower_idx)
                upper_ordered = self._sort_indices_by_xy_angle(points, upper_idx)

                edges = []

                for i in range(4):
                    a = lower_ordered[i]
                    b = lower_ordered[(i + 1) % 4]
                    edges.append((a, b))

                for i in range(4):
                    a = upper_ordered[i]
                    b = upper_ordered[(i + 1) % 4]
                    edges.append((a, b))

                # Connect corresponding vertices between layers by nearest XY.
                remaining_upper = upper_ordered.copy()
                for li in lower_ordered:
                    lxy = points[li, :2]
                    best = min(
                        remaining_upper,
                        key=lambda ui: np.linalg.norm(points[ui, :2] - lxy)
                    )
                    edges.append((li, best))
                    remaining_upper.remove(best)

                return edges

        return None

    def _sort_indices_by_xy_angle(self, points, indices):
        subset = points[indices, :2]
        cx = subset[:, 0].mean()
        cy = subset[:, 1].mean()

        return sorted(
            indices,
            key=lambda i: np.arctan2(points[i, 1] - cy, points[i, 0] - cx)
        )

    def _build_point_for_shape(self, shape, values):
        base = [values[0], values[1], values[2], 1.0]
        target_cols = shape.vertex.shape[1]

        if target_cols <= 4:
            return np.array([base], dtype=np.float32)

        # Preserve extra attributes (e.g., RGB) using the last vertex as template.
        extra = shape.vertex[-1, 4:target_cols].tolist()
        return np.array([base + extra], dtype=np.float32)

