from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *

from services.log_service import LogService
from src.utils.pipeline_3d import Pipeline3D


def apply_viewport_transform_3d(shape, viewport):
    """
    Aplica transformação de viewport 3D com rotação isométrica e normalização.
    Similar ao apply_viewport_transform mas para 3D.
    """
    xmin, ymin, xmax, ymax = viewport

    pipeline = Pipeline3D(xmin, ymin, xmax, ymax)
    
    # Usar o método transform do Pipeline3D que aplica todas as transformações
    # na ordem correta (rotação + normalização + viewport)
    vertex = pipeline.transform(shape.vertex)

    return vertex, pipeline


class ViewportWindow3DView(OpenGLFrame):
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

        self._display_3d()

    def _display_3d(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        points, pipeline = apply_viewport_transform_3d(self.shape, self.viewport)
        self._log_transform_3d(points, pipeline)

        glPointSize(2.0)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        
        # Usar a mesma lógica do Shape.render_3d()
        if self.shape.has_edge_sequence():
            for a, b in self.shape.edge_sequence:
                if points[a].shape[0] >= 7:
                    glColor3fv(points[a][4:7])
                else:
                    glColor3f(0.0, 0.0, 1.0)
                glVertex2f(points[a][0], points[a][1])

                if points[b].shape[0] >= 7:
                    glColor3fv(points[b][4:7])
                else:
                    glColor3f(0.0, 0.0, 1.0)
                glVertex2f(points[b][0], points[b][1])
        else:
            for v in points:
                if v.shape[0] >= 7:
                    glColor3fv(v[4:7])
                else:
                    glColor3f(0.0, 0.0, 1.0)
                glVertex2f(v[0], v[1])
        
        glEnd()
        glFlush()

    def _log_transform_3d(self, points, pipeline):
        if self._logged:
            return

        xmin, ymin, xmax, ymax = self.viewport
        self.log.header("VIEWPORT 3D (Isométrica)")
        self.log.step(f"Viewport: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")
        self.log.separator()
        self.log.step("Matriz de Rotação Isométrica:")
        self.log.matrix("M_iso", pipeline.isometric_rotation())
        self.log.step("Matriz de Normalização NDC:")
        self.log.matrix("M_normalize", pipeline.normalize_transformation())
        self.log.step("Matriz de Viewport (NDC → viewport):")
        self.log.matrix("M_viewport", pipeline.viewport_tranformation())
        self.log.step("Vértices originais:")
        self.log.matrix("V", self.shape.vertex)
        self.log.step("Resultado final (V'):")
        self.log.matrix("V'", points)
        self.log.separator()

        self._logged = True
