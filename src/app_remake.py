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

from src.views.main_frame import MainFrame

def main():
    root = Tk()
    root.title("testes")
    root.attributes("-zoomed", True)

    main_frame = MainFrame(root)
   
if __name__ == "__main__":
    main()