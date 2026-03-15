from tkinter import *
from src.components.shared.popup_frame import PopupFrame

class BezierFrame(PopupFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

    def open_popup(self):

       
        Label(self.popup, text="Point P0 (x0, y0):").grid(row=0, column=0, pady=5)
        self.ent_x0 = Entry(self.popup, width=6)
        self.ent_y0 = Entry(self.popup, width=6)
        self.ent_x0.grid(row=0, column=1)
        self.ent_y0.grid(row=0, column=2)

        
        Label(self.popup, text="Point P1 (x1, y1):").grid(row=1, column=0, pady=5)
        self.ent_x1 = Entry(self.popup, width=6)
        self.ent_y1 = Entry(self.popup, width=6)
        self.ent_x1.grid(row=1, column=1)
        self.ent_y1.grid(row=1, column=2)

        
        Label(self.popup, text="Point P2 (x2, y2):").grid(row=2, column=0, pady=5)
        self.ent_x2 = Entry(self.popup, width=6)
        self.ent_y2 = Entry(self.popup, width=6)
        self.ent_x2.grid(row=2, column=1)
        self.ent_y2.grid(row=2, column=2)

        
        Label(self.popup, text="Point P3 (x3, y3):").grid(row=3, column=0, pady=5)
        self.ent_x3 = Entry(self.popup, width=6)
        self.ent_y3 = Entry(self.popup, width=6)
        self.ent_x3.grid(row=3, column=1)
        self.ent_y3.grid(row=3, column=2)

        
        btn = Button(self.popup, text="Draw", command=self.get_input)
        btn.grid(row=4, column=0, columnspan=3, pady=12)

        
        self.popup.grid_columnconfigure(0, weight=1)
        self.popup.grid_columnconfigure(1, weight=1)
        self.popup.grid_columnconfigure(2, weight=1)

    def get_input(self):
        try:
            self.p0 = (float(self.ent_x0.get()), float(self.ent_y0.get()))
            self.p1 = (float(self.ent_x1.get()), float(self.ent_y1.get()))
            self.p2 = (float(self.ent_x2.get()), float(self.ent_y2.get()))
            self.p3 = (float(self.ent_x3.get()), float(self.ent_y3.get()))

            self.popup.destroy()

        except ValueError:
            print("Valores Inválidos")