from tkinter import *
from src.views.view_mode_view import ViewModeView
from src.views.edit_shape_view import EditShapeView 

class LateralBarView(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self.view_mode_view = ViewModeView(self)
        self.view_mode_view.grid(row=0, column=0)
         
        self.listbox = Listbox(self)
        self.listbox.grid(row=1, column=0)

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=1)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.edit_shape_view = EditShapeView(self)
        self.edit_shape_view.grid(row=3, column=0)
        

  
    