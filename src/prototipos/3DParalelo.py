import os
import sys
import platform
import logging

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'


import numpy as np

from typing import List

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from src.shape import Shape

class Camera:
    eye =    [100.0, 70.0, 100.0]    # afastada diagonalmente acima do centro
    center = [0.0, 0.0, 0.0]      # olhando para a origem
    up     = [0.0, 1.0, 0.0]      # vetor "para cima"

    def viewing_tranformation(self):
        self.eye = np.array(self.eye, dtype=float)
        self.center = np.array(self.center, dtype=float)
        self.up = np.array(self.up, dtype=float)

        # n = camera backward direction
        n = self.eye - self.center
        n = n / np.linalg.norm(n)

        # u = right vector
        u = np.cross(self.up, n)
        u = u / np.linalg.norm(u)

        # v = true up vector
        v = np.cross(n, u)

        return np.array([
            [u[0], u[1], u[2], -np.dot(u, self.eye)],
            [v[0], v[1], v[2], -np.dot(v, self.eye)],
            [n[0], n[1], n[2], -np.dot(n, self.eye)],
            [0, 0, 0, 1 ]
        ])
    
    def info(self):
        logging.info(f"Eye: {self.eye}")
        logging.info(f"Center: {self.center}")
        logging.info(f"Up: {self.up}")

class Screen:
    # Parâmetros da projeção
    fov    = np.radians(60)       # campo de visão
    aspect = 16/9                  # proporção da tela
    near   = 1.0                   # plano próximo (afastado para não cortar objetos próximos)
    far    = 100  

    def projection_transformation(self):
        t = np.tan(self.fov / 2)

        return np.array([
            [1/(t * self.aspect), 0,                 0,                           0],
            [0,              1/t,               0,                           0],
            [0,              0,       -(self.far+self.near)/(self.far-self.near),   -(2*self.far*self.near)/(self.far-self.near)],
            [0,              0,               -1,                           0]
        ], dtype=np.float32)
    
    def info(self):
        logging.info(f"Fov: {self.fov}")
        logging.info(f"Aspect: {self.aspect}")
        logging.info(f"Near: {self.near}")
        logging.info(f"Far: {self.far}")


class Window3D():
    x_min, y_min = 0, 0
    width, height = 800, 600
    camera: Camera = None
    screen: Screen = None
    shapes: List[Shape] = []

    def __init__(self, camera: Camera, screen: Screen):
        self.camera = camera
        self.screen = screen

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for shape in self.shapes:
            self.draw(shape)
        glFlush()

    def draw(self, shape: Shape):
        points = self.three_dimensional_viewing_pipeline(shape)

        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(2)
        glBegin(GL_LINES)
        if shape.has_edge_sequence():
            for a, b in shape.edge_sequence:
                glVertex2f(points[a][0], points[a][1])
                glVertex2f(points[b][0], points[b][1])
        else:
            for point in points:
                glVertex2f(point[0], point[1])
        glEnd()


    def three_dimensional_viewing_pipeline(self, shape: Shape):
        #modeling_transformation = None #Implementar ()
        #clipping = None #Implementar
 
        result = shape.vertex @ self.isometric_rotation().T

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
            [ np.sqrt(2)/2, 0,  np.sqrt(2)/2, 0],
            [ 0,             1,  0,             0],
            [-np.sqrt(2)/2, 0,  np.sqrt(2)/2,  0],
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

    def run(self):
        def keyboard(key, x, y):
            if key == GLUT_KEY_UP:
                self.camera.eye[1] += 2.2
            elif key == GLUT_KEY_LEFT:
                self.camera.eye[0] -= 2.2
            elif key == GLUT_KEY_RIGHT:
                self.camera.eye[0] += 2.2
            elif key == GLUT_KEY_DOWN:
                self.camera.eye[1] -= 2.2
            glutPostRedisplay()

        def mouse(button, state, x, y):
            if button == 3 and state == GLUT_DOWN:
                self.camera.eye[0] += 2.0
                self.camera.eye[2] += 2.0
            elif button == 4 and state == GLUT_DOWN:
                self.camera.eye[0] -= 2.0
                self.camera.eye[2] -= 2.0 
            glutPostRedisplay()

        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("Pipeline Manual")
        glutDisplayFunc(self.display)
        glutSpecialFunc(keyboard)
        glutMouseFunc(mouse)
        glutMainLoop()




axies = np.array([
    [0.0, 0.0, 0.0, 1.0],
    [1000.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1],
    [0.0, 10000.0, 0.0, 1],
    [0.0, 0.0, 0.0, 1],
    [0.0, 0.0, 10000.0, 1]
],dtype=np.float32)

cube = np.array([
    [ 25.0, -25.0, 25.0, 1.0],
    [ 25.0, -25.0, -25.0, 1.0],
    [ -25.0, -25.0, -25.0, 1.0],
    [ -25.0, -25.0, 25.0, 1.0],

    [ 25.0, 25.0, 25.0, 1.0],
    [ 25.0, 25.0, -25.0, 1.0],
    [ -25.0, 25.0, -25.0, 1.0],
    [ -25.0,  25.0, 25.0, 1.0],
], dtype=np.float32)

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # face baixa
    (4, 5), (5, 6), (6, 7), (7, 4),  # face alta
    (0, 4), (1, 5), (2, 6), (3, 7)   # conectar as faces
]

axies = Shape(matrix=axies, gl_option=GL_LINES)
shape = Shape(matrix=cube, gl_option=GL_LINES, edge_sequence=cube_edges)

camera = Camera()
screen = Screen()
window3D = Window3D(camera, screen)
window3D.shapes.append(axies)
window3D.shapes.append(shape)
window3D.run()