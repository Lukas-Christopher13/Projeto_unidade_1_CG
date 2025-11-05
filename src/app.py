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

from src.contexte_menu import ContextMenu
from src.shapes_lateral_bar import ShapesLateralBar

def main():
    root = Tk()
    root.title("testes")
    root.attributes("-zoomed", True)

    #Main Frame
    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
  
    #Main OpenGL
    gl_window = WindowTk(main_frame, bd=0, highlightthickness=0)
    gl_window.pack(side=LEFT, expand=True, fill=BOTH, padx=0, pady=0)

    #Lateral Bar
    shapes_lateral_bar = ShapesLateralBar(main_frame, gl_window=gl_window)

    #Listener 
    gl_window.add_listener(shapes_lateral_bar)

    contexte_menu = ContextMenu(gl_window)

    gl_window.animate = 1
    gl_window.mainloop()
 
if __name__ == "__main__":
    main()

#a clipping window seleciona oque queremos ver ea viewport indica onde vemos oque deve ser visto