from tkinter import *

from src.edite_shape import EditShape

class ShapesLateralBar(Frame):
    def __init__(self, parent, window_tk, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.widown_tk = window_tk

        lateralbar = Frame(self.parent, width=150)
        lateralbar.pack(side=TOP, fill=BOTH, padx=0, pady=0)

        main_frame = Frame(lateralbar)
        main_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.listbox = Listbox(main_frame)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        scrollbar = Scrollbar(main_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=LEFT, fill=BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind("<<ListboxSelect>>", self.select_shape)

        #####################################
        frame = Frame(self.parent, height=100)
        frame.pack(side=BOTTOM, fill=BOTH, padx=0, pady=0)

        btn_delete = Button(frame, text="delete", command=lambda: self.delete(self.selected))
        btn_delete.pack(pady=5)

        btn_change_color = Button(frame, text="change_color", command=self.test)
        btn_change_color.pack(pady=5)


    def update(self):
        self.listbox.delete(0, "end")
        for id, valor in enumerate(self.widown_tk.shapes):
            self.listbox.insert("end", str(id))

    def select_shape(self, event):
        select = self.listbox.curselection()
        if select:
            print(select)
            indice = select[0]
            valor = self.listbox.get(indice)
            self.selected = int(valor)
    
    def delete(self, id):
        self.widown_tk.delete_shape(id)
        
    def test():
        pass
