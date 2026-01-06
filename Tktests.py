import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *


class MyOpenGLFrame(OpenGLFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.animate = 0   # 🔴 sem loop
        self.lines = []    # 🔹 cena começa vazia

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)

    def redraw(self):
        print("REDRAW")

        self.tkMakeCurrent()

        w = self.winfo_width()
        h = self.winfo_height()

        glViewport(0, 0, w, h)
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 🔹 desenha tudo que existir na cena
        for (x1, y1, x2, y2) in self.lines:
            glBegin(GL_LINES)
            glColor3f(1, 0, 0)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glEnd()

        glFlush()

    def request_render(self):
        # 🔥 forma correta de pedir redraw no Tk
        self.event_generate("<Expose>")

    def add_line(self, x1, y1, x2, y2):
        self.lines.append((x1, y1, x2, y2))
        self.request_render()


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("OpenGLFrame sem flag artificial")
        self.geometry("600x400")

        self.gl = MyOpenGLFrame(self, width=400, height=300)
        self.gl.pack(side=TOP, fill=BOTH, expand=True)

        Button(self, text="Desenhar linha", command=self.draw).pack(pady=10)

    def draw(self):
        # 🔹 modifica o modelo
        self.gl.add_line(50, 50, 300, 300)


if __name__ == "__main__":
    App().mainloop()
