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
from utils.shape import Shape

from src.contexte_menu import ContextMenu
from src.shapes_lateral_bar import ShapesLateralBar

from src.backgrounds import cartesiam_plane


WIDTH = 800
HEIGHT = 600


def main():
    global vertices
    vertices = []

    root = Tk()
    root.title("testes")

    side_frame = Frame(root)
    side_frame.pack(side=LEFT, fill=Y, padx=0, pady=0)

    window = WindowTk(root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
    window.pack(side=LEFT, expand=True, fill=BOTH, padx=0, pady=0)
    window.add_background(cartesiam_plane) #passivel de melhorias

    shapes_lateral_bar = ShapesLateralBar(root)

    def action():
        pass

    def clear():
        window.clear_all()

    def add_shape():
        pass

    btn_action = Button(side_frame, text="action", command=action)
    btn_action.grid(row=0, column=0, columnspan=2, pady=10)

    btn_clear = Button(side_frame, text="clear", command=clear)
    btn_clear.grid(row=1, column=0, columnspan=2, pady=10)

    btn_add_shape = Button(side_frame, text="add shape", command=add_shape)
    btn_add_shape.grid(row=2, column=0, columnspan=2, pady=10)

    contexte_menu = ContextMenu(window)

    window.animate = 1
    window.mainloop()
 
if __name__ == "__main__":
    main()