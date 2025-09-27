from tkinter import *

class ShapesLateralBar(Frame):
    def __init__(self, parent, window_tk, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.widown_tk = window_tk

        lateralbar = Frame(self.parent, width=150)
        lateralbar.pack(side=LEFT, fill=BOTH, padx=0, pady=0)

        main_frame = Frame(lateralbar)
        main_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.listbox = Listbox(main_frame)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        scrollbar = Scrollbar(main_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=LEFT, fill=BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)

    def update(self):
        self.listbox.delete(0, "end")
        for id, valor in enumerate(self.widown_tk.shapes):
            self.listbox.insert("end", str(id))
