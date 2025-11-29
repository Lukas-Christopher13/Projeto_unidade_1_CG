import sys
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- Construção da matriz isométrica ortográfica (4x4) ---
theta_y = math.radians(45.0)                    # Ry = 45°
theta_x = math.atan(1.0 / math.sqrt(2.0))        # Rx = arctan(1/sqrt(2)) ≈ 35.264°

# Rotação em Y (4x4)
R_y = np.array([
    [ math.cos(theta_y), 0.0, -math.sin(theta_y), 0.0],
    [ 0.0,               1.0,  0.0,               0.0],
    [ math.sin(theta_y), 0.0,  math.cos(theta_y), 0.0],
    [ 0.0,               0.0,  0.0,               1.0]
], dtype=np.float32)

# Rotação em X (4x4)
R_x = np.array([
    [1.0, 0.0,               0.0,                0.0],
    [0.0, math.cos(theta_x), -math.sin(theta_x), 0.0],
    [0.0, math.sin(theta_x),  math.cos(theta_x), 0.0],
    [0.0, 0.0,               0.0,                1.0]
], dtype=np.float32)

R_iso = R_x @ R_y

# Projeção ortográfica que "zera" componente Z (mantemos coluna/linha homogênea)
P_ortho = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0],  # descarta Z
    [0.0, 0.0, 0.0, 1.0]
], dtype=np.float32)

M_iso_ortho = P_ortho @ R_iso  # matriz 4x4 final

# --- OpenGL / GLUT ---
width, height = 800, 600

angle = 0.0  # opcional: girar o cubo antes da projeção (apenas para dinâmica)

def init_gl():
    glClearColor(0.95, 0.95, 0.95, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

def load_isometric_projection_matrix():
    # OpenGL espera matriz em column-major; numpy é row-major -> usamos .T
    mat = M_iso_ortho.T.flatten().astype(np.float32)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Carregamos a matriz isométrica diretamente como matriz de projeção
    glMultMatrixf(mat)
    # Como a matriz z foi zerada, o volume de recorte padrão pode ser não apropriado;
    # portanto aplicamos um scale/translate simples para ajustar a cena na viewport.
    # (opcional) expandir coordenadas para caber na janela:
    # aqui mantemos identidade no modelview para desenhar nas coordenadas transformadas.
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_axes(length=1.5):
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # X - vermelho
    glColor3f(0.8, 0.1, 0.1)
    glVertex3f(0,0,0); glVertex3f(length,0,0)
    # Y - verde
    glColor3f(0.1,0.7,0.1)
    glVertex3f(0,0,0); glVertex3f(0,length,0)
    # Z - azul
    glColor3f(0.1,0.1,0.9)
    glVertex3f(0,0,0); glVertex3f(0,0,length)
    glEnd()

def draw_cube(size=1.0):
    # Desenha um cubo com faces coloridas (centrado na origem)
    hs = size / 2.0
    vertices = [
        [-hs, -hs, -hs],
        [ hs, -hs, -hs],
        [ hs,  hs, -hs],
        [-hs,  hs, -hs],
        [-hs, -hs,  hs],
        [ hs, -hs,  hs],
        [ hs,  hs,  hs],
        [-hs,  hs,  hs],
    ]
    faces = [
        (0,1,2,3),  # back
        (4,5,6,7),  # front
        (0,4,7,3),  # left
        (1,5,6,2),  # right
        (3,2,6,7),  # top
        (0,1,5,4),  # bottom
    ]
    colors = [
        (0.8,0.3,0.3),
        (0.3,0.8,0.3),
        (0.3,0.3,0.8),
        (0.9,0.8,0.3),
        (0.6,0.3,0.9),
        (0.3,0.9,0.9),
    ]
    glBegin(GL_QUADS)
    for f_idx, face in enumerate(faces):
        glColor3f(*colors[f_idx % len(colors)])
        for vi in face:
            glVertex3f(*vertices[vi])
    glEnd()

def display():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    # opcional: um pequeno giro no modelview antes da projeção (não necessário).
    # glRotatef(angle, 0.0, 1.0, 0.0)

    # desenha eixos para referência (eles também serão projetados)
    draw_axes(1.2)
    # desenha cubo
    draw_cube(1.0)

    glPopMatrix()
    glutSwapBuffers()

def idle():
    global angle
    #angle += 0.1
    glutPostRedisplay()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    # Ao redimensionar, recarregamos a matriz isométrica para manter proporção
    load_isometric_projection_matrix()

def keyboard(key, x, y):
    if key == b'\x1b' or key == b'q':  # ESC ou q para sair
        sys.exit(0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Isometric Orthographic Projection - Cube (PyOpenGL)")
    init_gl()
    load_isometric_projection_matrix()
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
