from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from utils.backgrounds import cartesiam_plane
from src.models.gl_window_model import singleton
from src.models.shape import Shape

from src.utils.shape_factory_3d import ShapeFactory3D

class GlWindowView(OpenGLFrame):
    window_mode = "3d"

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        
    def initgl(self):
        glClearColor (1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(-1000, 1000, -1000, 1000) # Passar esse valor
        glMatrixMode (GL_MODELVIEW)

        glClearColor(1, 1, 1, 1)

    def redraw(self):
        if self.window_mode == "2d":
            self.redraw_2d()
        else:
            self.redraw_3d()

    def redraw_2d(self):
        width = self.winfo_width()
        height = self.winfo_height()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.resize_window(width, height)

        cartesiam_plane(2000, 2000)
        self.controller.model.render_shapes()
       
        glFlush()

    def redraw_3d(self):
        self.x_min, self.y_min = 0, 0
        self.width, self.height = 800, 600

        singleton.use_3d_axies()
        singleton.add_shape(ShapeFactory3D.cube())

        self.display_3d()
    
    def resize_window(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = width / height

        if(width >= height):
            gluOrtho2D(-1000 * aspect, 1000 * aspect, -1000, 1000)
        else:
            gluOrtho2D(-1000, 1000, -1000 / aspect, 1000 / aspect)

    def set_controller(self, controller):
        self.controller = controller

    
    def display_3d(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for background in singleton.backgrounds:
            self.draw_3d(background)

        for shape in singleton.shapes:
            self.draw_3d(shape)

        glFlush()

    def draw_3d(self, shape):
        points = self.pipileine_3d(shape.vertex)

        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(2)
        glBegin(GL_LINES)
        if  shape.has_edge_sequence():
            for a, b in shape.edge_sequence:
                glVertex2f(points[a][0], points[a][1])
                glVertex2f(points[b][0], points[b][1])
        else:
            for point in points:
                glVertex2f(point[0], point[1])
        glEnd()

    def pipileine_3d(self, np_matrix):
        #modeling_transformation = None #Implementar ()
        #clipping = None #Implementar
 
        result = np_matrix @ self.isometric_rotation().T

        # 2 — Projeção ortográfica paralela
        result = result @ self.orthographic_projection().T

        # 3 — Normalização NDC
        result = np.array([self.normalize_to_ndc(v) for v in result])

        # 4 — Viewport
        result = result @ self.viewport_transformation().T

        # --Ordem--
        #Modeling Transformation
        #Viewing Transformation
        #Projection Transformation
        #Normalization Transformation
        #Viewport Transformation
        #Clipping Transformation 

        return result


    def orthographic_projection(self, l=-200, r=200, b=-200, t=200, n=-500, f=500):
        return np.array([
            [2/(r-l), 0,         0,         -(r+l)/(r-l)],
            [0,       2/(t-b),   0,         -(t+b)/(t-b)],
            [0,       0,        -2/(f-n),   -(f+n)/(f-n)],
            [0,       0,         0,          1]
        ], dtype=np.float32)
    
    def translate_to_origin(self, cx, cy, cz):
        return np.array([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 1, -cz],
            [0, 0, 0,   1]
        ], dtype=np.float32)
    
    def isometric_rotation(self):
        # Rotação em Y: 45°
        Ry = np.array([
            [ np.sqrt(2)/2, 0,  -np.sqrt(2)/2, 0],
            [ 0,             1,  0,             0],
            [ np.sqrt(2)/2, 0,  np.sqrt(2)/2,  0],
            [ 0,             0,  0,             1]
        ], dtype=np.float32)

        # Rotação em X: 35.264° (arctan(1/sqrt(2)))
        cosx = np.sqrt(2/3)
        sinx = 1/np.sqrt(3)

        Rx = np.array([
            [1,    0,     0,     0],
            [0,  cosx, -sinx,    0],
            [0,  sinx,  cosx,    0],
            [0,    0,     0,     1]
        ], dtype=np.float32)

        return Rx @ Ry

    def normalize_to_ndc(self, v):
        """
        Converte um ponto em Clip Space (x, y, z, w)
        para NDC ao dividir tudo por w.
        """
        x, y, z, w = v
        
        if w == 0:
            raise ValueError("w = 0 → não é possível dividir")

        return np.array([x/w, y/w, z/w, 1.0], dtype=np.float32)
    
    def viewport_transformation(self):
        """
        Retorna a matriz 4x4 de transformação de viewport.
        
        Parâmetros:
            x_min  → posição inicial do viewport no eixo X
            y_min  → posição inicial do viewport no eixo Y
            width  → largura do viewport (em pixels)
            height → altura do viewport (em pixels)
        """

        # Metade das dimensões
        w2 = self.width / 2.0
        h2 = self.height / 2.0

        # A matriz de viewport é uma transformação afim:
        M = np.array([
            [ w2,   0.0, 0.0, self.x_min + w2 ],
            [ 0.0,  h2, 0.0, self.y_min + h2 ],  # OBS: sinal negativo para inverter Y
            [ 0.0,  0.0, 0.5, 0.5       ], # mapeia Z de [-1,1] para [0,1]
            [ 0.0,  0.0, 0.0, 1.0       ]
        ], dtype=np.float32)

        return M


