from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *

from services.log_service import LogService
from src.utils.matrix_transform import basic_scaling, translate


def apply_viewport_transform(shape, viewport):
    xmin, ymin, xmax, ymax = viewport

    viewport_width = max(1, xmax - xmin)
    viewport_height = max(1, ymax - ymin)
    aspect = viewport_width / viewport_height

    world_xmin, world_ymin = -1000.0, -1000.0
    world_xmax, world_ymax = 1000.0, 1000.0

    if aspect >= 1:
        world_xmin *= aspect
        world_xmax *= aspect
    else:
        world_ymin /= aspect
        world_ymax /= aspect

    sx = 2 / (world_xmax - world_xmin)
    sy = 2 / (world_ymax - world_ymin)
    n_cx = (world_xmin + world_xmax) / 2
    n_cy = (world_ymin + world_ymax) / 2

    normalize = translate(n_cx, n_cy) @ basic_scaling(sx, sy) @ translate(0.0, 0.0)

    sx_vp = (xmax - xmin) / 2
    sy_vp = (ymax - ymin) / 2
    tx_vp = (xmax + xmin) / 2
    ty_vp = (ymax + ymin) / 2

    viewport_m = translate(tx_vp, ty_vp) @ basic_scaling(sx_vp, sy_vp) @ translate(0.0, 0.0)

    vertex = shape.vertex.copy()
    vertex[:, :4] = vertex[:, :4] @ normalize.T
    vertex[:, :4] = vertex[:, :4] @ viewport_m.T

    return vertex, normalize, viewport_m


class ViewportWindowView(OpenGLFrame):
    def __init__(self, root, viewport, shape, **kwargs):
        super().__init__(root, **kwargs)
        self.viewport = viewport
        self.shape = shape
        self.log = LogService()
        self._logged = False

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)

    def request_render(self):
        self.event_generate("<Expose>")

    def redraw(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        if self.width <= 0 or self.height <= 0:
            return

        self._display_2d()

    def _display_2d(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        points, normalize_m, viewport_m = apply_viewport_transform(self.shape, self.viewport)
        self._log_transform(points, normalize_m, viewport_m)

        glPointSize(3.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(self.shape.gl_option)
        for v in points:
            if v.shape[0] >= 7:
                glColor3fv(v[4:7])
            else:
                glColor3f(0.0, 0.0, 1.0)
            glVertex2f(v[0], v[1])
        glEnd()

        glFlush()

    def _log_transform(self, points, normalize_m, viewport_m):
        if self._logged:
            return

        xmin, ymin, xmax, ymax = self.viewport
        self.log.header("VIEWPORT 2D")
        self.log.step(f"Viewport: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")
        self.log.separator()
        self.log.step("Matriz de Viewport (NDC → viewport):")
        self.log.matrix("M_viewport", viewport_m)
        self.log.step("Matriz do Objeto:")
        self.log.matrix("V", self.shape.vertex)
        self.log.step("Resultado final (V'):")
        self.log.matrix("V'", points)
        self.log.separator()

        self._logged = True
