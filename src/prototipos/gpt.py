import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'


import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

angle = 0.0

# MODELING TRANSFORMATION
#Aplica as tranformações no objeto, Primeira etapa
def modeling_transformation():
    return

#Viewing Transformation
#center -> ponto onde a camera olha > direção de olhar
#up -> controlar a posição da tela;
#eye -> posição da camera:
def viewing_tranformation(eye, center, up):
    eye = np.array(eye, dtype=float)
    center = np.array(center, dtype=float)
    up = np.array(up, dtype=float)

    # n = camera backward direction
    n = eye - center
    n = n / np.linalg.norm(n)

    # u = right vector
    u = np.cross(up, n)
    u = u / np.linalg.norm(u)

    # v = true up vector
    v = np.cross(n, u)

    M = np.array([
        [ u[0],  v[0],  n[0],  0.0 ],
        [ u[1],  v[1],  n[1],  0.0 ],
        [ u[2],  v[2],  n[2],  0.0 ],
        [-np.dot(u, eye), -np.dot(v, eye), -np.dot(n, eye), 1.0 ]
    ])

    return M

#fov = field of view, abertura da câmera
#aspect ratio = largura/altura
#near / far = planos de corte
#(objetos fora disso são descartados)
def projection_transformation(fov, aspect, near, far):
    t = np.tan(fov / 2)

    return np.array([
        [1/(t * aspect), 0,                 0,                           0],
        [0,              1/t,               0,                           0],
        [0,              0,       -(far+near)/(far-near),   -(2*far*near)/(far-near)],
        [0,              0,               -1,                           0]
    ], dtype=np.float32)
#Um vértice (x, y, z, w) está dentro do frustum SE, e somente se:
# -w ≤ x ≤ w
# -w ≤ y ≤ w
# -w ≤ z ≤ w
def cliping():
    pass

def normalize_to_ndc(v):
    """
    Converte um ponto em Clip Space (x, y, z, w)
    para NDC ao dividir tudo por w.
    """
    x, y, z, w = v
    
    if w == 0:
        raise ValueError("w = 0 → não é possível dividir")

    return np.array([x/w, y/w, z/w, 1.0], dtype=np.float32)

import numpy as np

#Viewport Transformation
def viewport_transformation(x_min, y_min, width, height):
    """
    Retorna a matriz 4x4 de transformação de viewport.
    
    Parâmetros:
        x_min  → posição inicial do viewport no eixo X
        y_min  → posição inicial do viewport no eixo Y
        width  → largura do viewport (em pixels)
        height → altura do viewport (em pixels)
    """

    # Metade das dimensões
    w2 = width / 2.0
    h2 = height / 2.0

    # A matriz de viewport é uma transformação afim:
    M = np.array([
        [ w2,   0.0, 0.0, x_min + w2 ],
        [ 0.0, -h2, 0.0, y_min + h2 ],  # OBS: sinal negativo para inverter Y
        [ 0.0,  0.0, 0.5, 0.5        ], # mapeia Z de [-1,1] para [0,1]
        [ 0.0,  0.0, 0.0, 1.0        ]
    ], dtype=np.float32)

    return M



def pipline():
    cube = np.array([
        [ 9.0,  4.0, -4.0, 1.0],
        [11.0,  4.0, -4.0, 1.0],
        [11.0,  6.0, -4.0, 1.0],
        [ 9.0,  6.0, -4.0, 1.0],

        [ 9.0,  4.0, -2.0, 1.0],
        [11.0,  4.0, -2.0, 1.0],
        [11.0,  6.0, -2.0, 1.0],
        [ 9.0,  6.0, -2.0, 1.0],
    ], dtype=np.float32)

    eye    = [4.0, 4.0, 4.0]
    center = [0.0, 0.0, 0.0]
    up     = [0.0, 1.0, 0.0]

    fov    = np.radians(45)   # ← precisa estar em radianos (altera)
    aspect = 16/9
    near   = 0.1
    far    = 100

    x_min  = 0
    y_min  = 0
    width  = 800
    height = 600

    #M_model = modeling_transformation()
    M_view  = viewing_tranformation(eye, center, up)
    M_proj  = projection_transformation(fov, aspect, near, far)
    M_vp    = viewport_transformation(x_min, y_min, width, height)

    cur = cube.copy()
    print("World:\n", cur)

    # Model
    # cur = cur @ M_model.T
    # print("\nModel:\n", cur)

    # View
    cur = cur @ M_view.T
    print("\nView:\n", cur)

    # Projection
    cur = cur @ M_proj.T
    print("\nProjection:\n", cur)

    # NDC normalization (divide by w)
    cur = np.array([normalize_to_ndc(v) for v in cur])
    print("\nNDC:\n", cur)

    # Viewport
    cur = cur @ M_vp.T
    print("\nViewport:\n", cur)

    return cur

width, height = 800, 600

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # <<< COORDENADAS DE TELA >>>
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Roda o pipeline
    points = pipline()

    # Desenha os vértices
    glPointSize(8)
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])  
    glEnd()

    edges = [
        (0, 1), (1, 5), (5, 4), (4, 0),  # frente
        (2, 3), (3, 7), (7, 6), (6, 2),  # trás
        (0, 2), (1, 3), (4, 6), (5, 7)   # conecta frente ↔ trás
    ]

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    for a, b in edges:
        glVertex2f(points[a][0], points[a][1])
        glVertex2f(points[b][0], points[b][1])
    glEnd()

    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow("Pipeline Manual")
    glutDisplayFunc(display)
    glutMainLoop()

main()

