import numpy as np

from src.utils.matrix_transform import basic_scaling, translate

INSIDE = 0b0000
LEFT   = 0b0001
RIGHT  = 0b0010
BOTTOM = 0b0100
TOP    = 0b1000

class Pipeline2D:
    world_xmin, world_ymin = -1000, -1000
    world_xmax, world_ymax = 1000, 1000

    def __init__(self, viewport_xmin, viewport_ymin, viewport_xmax, viewport_ymax):
        self.viewport_xmin = viewport_xmin
        self.viewport_ymin = viewport_ymin
        self.viewport_xmax = viewport_xmax
        self.viewport_ymax = viewport_ymax

        viewport_width = max(1, self.viewport_xmax - self.viewport_xmin)
        viewport_height = max(1, self.viewport_ymax - self.viewport_ymin)
        aspect = viewport_width / viewport_height

        if aspect >= 1:
            self.world_xmin =  self.world_xmin * aspect
            self.world_xmax =  self.world_xmax * aspect
            self.world_ymin =  self.world_ymin
            self.world_ymax =  self.world_ymax
        else:
            self.world_xmin =  self.world_xmin
            self.world_xmax =  self.world_xmax
            self.world_ymin =  self.world_ymin / aspect
            self.world_ymax =  self.world_ymax / aspect

    def transform(self, shape):
        #modeling_transformation = None #Implementar () #aparentemente não precisa - o Shape Ja faz!!!

        vertex = shape.vertex.copy()

        # self.cohen_sutherland_clip(
        #     np_matrix_copy,
        #     self.world_xmin, self.world_ymin,
        #     self.world_xmax, self.world_ymax
        # )

        vertex[:, :4] = vertex[:, :4] @ self.normalize_transformation().T

        vertex[:, :4] = vertex[:, :4] @ self.viwport_transformation().T

        return vertex

    #talvez eu tenha que usar as formulas que centralizem

    def normalize_transformation(self):
        sx = 2 / (self.world_xmax - self.world_xmin)
        sy = 2 / (self.world_ymax - self.world_ymin)

        n_cx = (self.world_xmin + self.world_xmax) / 2
        n_cy = (self.world_ymin + self.world_ymax) / 2

        w_cx = (-1 + 1) / 2
        w_cy = (-1 + 1) / 2

        return translate(n_cx, n_cy) @ basic_scaling(sx, sy) @ translate(-w_cx, -w_cy)

    def viwport_transformation(self):
        sx = (self.viewport_xmax - self.viewport_xmin) / 2
        sy = (self.viewport_ymax - self.viewport_ymin) / 2

        tx = (self.viewport_xmax + self.viewport_xmin) / 2
        ty = (self.viewport_ymax + self.viewport_ymin) / 2

        n_cx = (-1 + 1) / 2
        n_cy = (-1 + 1) / 2

        return translate(tx, ty) @ basic_scaling(sx, sy) @ translate(-n_cx, -n_cy)

    def viewport_to_world(self, x, y):
        M = self.viwport_transformation() @ self.normalize_transformation()
        inv_M = np.linalg.inv(M)
        v = np.array([x, y, 0.0, 1.0], dtype=np.float32)
        world = v @ inv_M.T
        return world[0], world[1]

    def cohen_sutherland_clip(self, np_matrix, xmin, ymin, xmax, ymax):
        x1, y1 = np_matrix[0][0], np_matrix[0][1]
        x2, y2 = np_matrix[1][0], np_matrix[1][1]

        out1 = self.compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
        out2 = self.compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

        while True:
            # ✅ 1. Aceitação trivial
            if (out1 | out2) == 0:
                return x1, y1, x2, y2

            # ❌ 2. Rejeição trivial
            if (out1 & out2) != 0:
                return None

            # 🔄 3. Recorte parcial
            out = out1 if out1 != 0 else out2

            if out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax

            elif out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin

            elif out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax

            elif out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if out == out1:
                old = (np_matrix[0][0], np_matrix[0][1])
                new = (x, y)
                self.print_clipped(old, new)

                x1, y1 = x, y
                np_matrix[0][0], np_matrix[0][1] = x1, y1

                out1 = self.compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                old = (np_matrix[0][0], np_matrix[0][1])
                new = (x, y)
                self.print_clipped(old, new)

                x2, y2 = x, y
                np_matrix[1][0], np_matrix[1][1] = x2, y2
                out2 = self.compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

    def compute_outcode(self, x, y, xmin, ymin, xmax, ymax):
        code = INSIDE

        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT

        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP

        return code

    def print_clipped(self, old, new):
        print(f"Clipped: ({old[0]:.2f}, {old[1]:.2f}) => ({new[0]:.2f}, {new[1]:.2f})")

#o window seleciona uma parte da cena no mundo
#o viewport exibe essa parte da sena
