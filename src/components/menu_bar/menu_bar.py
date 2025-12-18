from tkinter import *

class MenuBar(Menu):
    def __init__(self, root, controller):
        super().__init__(root)
        
        self.controller = controller

        self._create_options_menu()

    def _create_options_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="3D", command=self.controller.open_3d)



