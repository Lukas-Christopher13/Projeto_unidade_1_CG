import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'


import numpy as np
from math import cos, sin, radians
from OpenGL.GL import *
from OpenGL.GLUT import *

# =====================================================
# VÉRTICES: [x, y, z, w, r, g, b]
# Coordenadas normalizadas (NDC)
# =====================================================
vertices = np.array([
    [-0.5, -0.5, 0.0, 1.0,   1.0, 0.0, 0.0],  # vermelho
    [ 0.5, -0.5, 0.0, 1.0,   0.0, 1.0, 0.0],  # verde
    [ 0.0,  0.5, 0.0, 1.0,   0.0, 0.0, 1.0],  # azul
], dtype=float)

# =====================================================
# MATRIZ DE TRANSFORMAÇÃO (4x4)
# Rotação em Z + Translação
# =====================================================
def create_transform(angle_deg, tx, ty):
    a = radians(angle_deg)
    return np.array([
        [ cos(a), -sin(a), 0.0, tx],
        [ sin(a),  cos(a), 0.0, ty],
        [ 0.0,     0.0,    1.0, 0.0],
        [ 0.0,     0.0,    0.0, 1.0],
    ], dtype=float)

# =====================================================
# APLICA TRANSFORMAÇÃO (SÓ NA POSIÇÃO)
# =====================================================
def apply_transform(vertices, M):
    for v in vertices:
        pos = v[0:4]          # x, y, z, w
        v[0:4] = M @ pos      # transforma apenas posição

# =====================================================
# RENDERIZAÇÃO
# =====================================================
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    for v in vertices:
        glColor3fv(v[4:7])    # cor
        glVertex3fv(v[0:3])   # posição
    glEnd()

    glFlush()

# =====================================================
# MAIN
# =====================================================
def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"OpenGL - Coordenadas Homogeneas + Cores")

    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Cria e aplica uma transformação qualquer
    M = create_transform(
        angle_deg=45,   # rotação
        tx=0.2,         # translação X
        ty=0.1          # translação Y
    )
    apply_transform(vertices, M)

    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
