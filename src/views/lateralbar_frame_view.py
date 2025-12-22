from tkinter import *
from src.shape_controller import EditShape

class LateralBarView(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
         
        self.listbox = Listbox(self)
        self.listbox.grid(row=0, column=0)

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        # edit_shape = EditShape(self, gl_window)
        # edit_shape.grid(row=1, column=0)

  
        