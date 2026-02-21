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

from components.contexte_menu_frame import ContextMenu
from components.shapes_lateral_bar_frame import ShapesLateralBar
from components.terminal_frame import TerminalFrame

def main():
    root = Tk()
    root.title("Computação Gráfica - Projeto Unidade 1")
    if so == "Linux":
        root.attributes("-zoomed", True)
    else:
        root.state("zoomed")

    #Main Frame
    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ── Layout vertical: Canvas (topo) + Terminal (base) ──
    paned = PanedWindow(main_frame, orient=VERTICAL, sashwidth=4, bg="#45475a")
    paned.pack(side=LEFT, expand=True, fill=BOTH)

    #Main OpenGL
    gl_window = WindowTk(paned, bd=0, highlightthickness=0)
    paned.add(gl_window, stretch="always")

    # Terminal de Logs
    terminal = TerminalFrame(paned)
    paned.add(terminal, height=250, stretch="never")

    #Lateral Bar
    shapes_lateral_bar = ShapesLateralBar(main_frame, gl_window=gl_window)

    #Listener 
    gl_window.add_listener(shapes_lateral_bar)

    contexte_menu = ContextMenu(gl_window)

    gl_window.animate = 1
    gl_window.mainloop()
 
if __name__ == "__main__":
    main()