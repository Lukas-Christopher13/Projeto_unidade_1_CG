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

axies = np.array([
    [1000.0, 0.0, 0.0, 1],
    [-1000.0, 0.0, 0.0, 1],
    [0.0, 1000.0, 0.0, 1],
    [0.0, -1000.0, 0.0, 1],
    [0.0, 0.0, 1000.0, 1],
    [0.0, 0.0, -1000.0, 1]
],dtype=np.float32)

cube = np.array([
    [ 50.0, 0.0, 0.0, 1.0],
    [ 0.0,  0.0,  50.0, 1.0],
    [ -50.0,  0.0,  0.0, 1.0],
    [ 0.0,  6.0, -50.0, 1.0],

    [ 50.0, 50.0, 0.0, 1.0],
    [ 0.0,  50.0,  50.0, 1.0],
    [-50.0,  50.0,  0.0, 1.0],
    [ 0.0,  50.0, -50.0, 1.0],
], dtype=np.float32)


    # edges = [
    #     (0, 1), (1, 2), (2, 3), (3, 0),  # frente
    #     (4, 5), (5, 6), (6, 7), (7, 4),  # trás
    #     (0, 4), (1, 5), (2, 6), (3, 7)   # conecta frente ↔ trás
    # ]

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
        [u[0], u[1], u[2], -np.dot(u, eye)],
        [v[0], v[1], v[2], -np.dot(v, eye)],
        [n[0], n[1], n[2], -np.dot(n, eye)],
        [0, 0, 0, 1 ]
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
        [ 0.0,  h2, 0.0, y_min + h2 ],  # OBS: sinal negativo para inverter Y
        [ 0.0,  0.0, 0.5, 0.5       ], # mapeia Z de [-1,1] para [0,1]
        [ 0.0,  0.0, 0.0, 1.0       ]
    ], dtype=np.float32)

    return M



def pipline(eye, object):
    cur = object.copy()
    print(f"eye:{eye}")

    #eye    = [10.0, 10.0, 10.0]   # afastada diagonalmente acima do centro
    center = [0.0, 0.0, 0.0]      # olhando para a origem
    up     = [0.0, 1.0, 0.0]      # vetor "para cima"

    # Parâmetros da projeção
    fov    = np.radians(60)       # campo de visão
    aspect = 16/9                  # proporção da tela
    near   = 1.0                   # plano próximo (afastado para não cortar objetos próximos)
    far    = 100  

    x_min  = 0
    y_min  = 0
    width  = 800
    height = 600

    #M_model = modeling_transformation()
    M_view  = viewing_tranformation(eye, center, up)
    M_proj  = projection_transformation(fov, aspect, near, far)
    M_vp    = viewport_transformation(x_min, y_min, width, height)

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

def display(eye):
    glClear(GL_COLOR_BUFFER_BIT)

    # <<< COORDENADAS DE TELA >>>
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Roda o pipeline
    points = pipline(eye, cube)
    

    # Desenha os vértices
    glPointSize(8)
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])  
    glEnd()

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # frente
        (4, 5), (5, 6), (6, 7), (7, 4),  # trás
        (0, 4), (1, 5), (2, 6), (3, 7)   # conecta frente ↔ trás
    ]

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    for a, b in edges:
        glVertex2f(points[a][0], points[a][1])
        glVertex2f(points[b][0], points[b][1])
    glEnd()

    points2 = pipline(eye, axies)

    glPointSize(8)
    glBegin(GL_LINES)
    for p in points2:
        glVertex2f(p[0], p[1])  
    glEnd()


    glFlush()


def main():
    eye = [100.0, 70.0, 100.0] 

    def keyboard(key, x, y):
        if key == GLUT_KEY_UP:
            eye[1] += 2.2
        elif key == GLUT_KEY_LEFT:
            eye[0] -= 2.2
        elif key == GLUT_KEY_RIGHT:
            eye[0] += 2.2
        elif key == GLUT_KEY_DOWN:
            eye[1] -= 2.2
        glutPostRedisplay()

    def mouse(button, state, x, y):
        if button == 3 and state == GLUT_DOWN:
            eye[0] += 2.0
            eye[2] += 2.0
        elif button == 4 and state == GLUT_DOWN:
            eye[0] -= 2.0
            eye[2] -= 2.0 
        glutPostRedisplay()

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow("Pipeline Manual")
    glutDisplayFunc(lambda: display(eye))
    glutSpecialFunc(keyboard)
    glutMouseFunc(mouse)
    glutMainLoop()


main()

