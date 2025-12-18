from tkinter import *

from src.shape_controller import EditShape

from src.controllers.lateral_bar_controller import LateralBarController

class LateralBar(Frame):
    lateral_bar_controller = LateralBarController()

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        #Reformular
        self.gl_window = root.gl_window
        self.gl_window.add_listener(self)

        #Transformar isso em componente!
        self.listbox = Listbox(self)
        self.listbox.grid(row=0, column=0)

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.select_shape)

        #Adicionar os outros inputs aqui!
        edit_shape = EditShape(self)
        edit_shape.grid(row=1, column=0)

    def update(self):
        self.listbox.delete(0, "end")
        for id, valor in enumerate(self.gl_window.shapes):
            self.listbox.insert("end", str(id))

    def select_shape(self, event):
        select = self.listbox.curselection()
        if select:
            indice = select[0]
            valor = int(self.listbox.get(indice))
            self.gl_window.set_selected(valor)