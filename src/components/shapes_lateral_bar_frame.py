from tkinter import *

from src.utils.windowtk import WindowTk
from shape_controller import EditShape

class ShapesLateralBar(Frame):
    def __init__(self, main_frame, **kwargs):
        super().__init__(main_frame, **kwargs)
        self.gl_window = main_frame.gl_window

        #reformular
        self.gl_window.add_listener(self)

        lateralbar = Frame(self, width=300)
        lateralbar.pack(side=TOP, fill=BOTH, padx=0, pady=0)

        main_frame = Frame(lateralbar)
        main_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.listbox = Listbox(main_frame)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        scrollbar = Scrollbar(main_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=LEFT, fill=BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind("<<ListboxSelect>>", self.select_shape)

        edit_shape = EditShape(self, self.gl_window)

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