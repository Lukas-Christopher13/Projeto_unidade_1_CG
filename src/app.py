import os
import sys
import platform

import numpy as np

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

from tkinter import * 
from OpenGL.GL import *
from OpenGL.GLU import *

from utils.windowtk import WindowTk

TRIANGLE = np.array([
    [ 0.0,  0.5, 0.0, 1.0],
    [-0.5, -0.5, 0.0, 1.0],
    [ 0.5, -0.5, 0.0, 1.0],
], dtype=np.float32)

SQUARE = np.array([
    [-0.5,  0.5, 0.0, 1.0],  
    [-0.5, -0.5, 0.0, 1.0],  
    [ 0.5, -0.5, 0.0, 1.0],  
    [ 0.5,  0.5, 0.0, 1.0],  
], dtype=np.float32)


WIDTH = 800
HEIGHT = 600


def main():
    global vertices
    vertices = []

    root = Tk()
    root.title("testes")

    window = WindowTk(root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
    window.pack(side=RIGHT, expand=True, fill=BOTH, padx=0, pady=0)

    side_frame = Frame(root)
    side_frame.pack(side=LEFT, fill=Y, padx=0, pady=0) 

    def action():
        window.update(GL_TRIANGLE_FAN, SQUARE)

    def clear():
        window.clear()

    btn_action = Button(side_frame, text="action", command=action)
    btn_action.grid(row=0, column=0, columnspan=2, pady=10)

    btn_clear = Button(side_frame, text="clear", command=clear)
    btn_clear.grid(row=1, column=0, columnspan=2, pady=10)

    window.animate = 1
    window.mainloop()
 
if __name__ == "__main__":
    main()