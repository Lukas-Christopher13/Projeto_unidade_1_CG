import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

from tkinter import * 
from OpenGL.GL import *
from OpenGL.GLU import *

from src.controllers.main_frame_controller import MainFrameController

def main():
    root = Tk()
    root.title("Computação Gráfica - Projeto Unidade 1")
    if so == "Linux":
        root.attributes("-zoomed", True)
    else:
        root.state("zoomed")

    main_frame_controller = MainFrameController(root)
    main_frame_controller.run()
   
if __name__ == "__main__":
    main()