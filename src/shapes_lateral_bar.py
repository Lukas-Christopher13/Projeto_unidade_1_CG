from tkinter import *

class ShapesLateralBar(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        lateralbar = Frame(self.parent, width=150)
        lateralbar.pack(side=LEFT, fill=BOTH, padx=0, pady=0)

        main_frame = Frame(lateralbar, bg="#ffffff")
        main_frame.pack(side=LEFT, fill=BOTH, expand=True)

        listbox = Listbox(main_frame)
        listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        scrollbar = Scrollbar(main_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=LEFT, fill=BOTH)
        listbox.config(yscrollcommand=scrollbar.set)

        valores = [f"Item {i}" for i in range(0, 21)]
        for valor in valores:
            listbox.insert("end", valor)
