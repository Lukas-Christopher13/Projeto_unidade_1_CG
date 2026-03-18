from tkinter import *
from src.components.shared.popup_frame import PopupFrame

class EllipseFrame(PopupFrame):
    def open_popup(self):
        Label(self.popup, text="Center X:").grid(row=0, column=0)
        self.ent_xc = Entry(self.popup, width=6)
        self.ent_xc.grid(row=0, column=1)
        self.ent_xc.insert(0, "0")

        Label(self.popup, text="Center Y:").grid(row=1, column=0)
        self.ent_yc = Entry(self.popup, width=6)
        self.ent_yc.grid(row=1, column=1)
        self.ent_yc.insert(0, "0")

        Label(self.popup, text="Radius X:").grid(row=2, column=0)
        self.ent_rx = Entry(self.popup, width=6)
        self.ent_rx.grid(row=2, column=1)
        self.ent_rx.insert(0, "200")

        Label(self.popup, text="Radius Y:").grid(row=3, column=0)
        self.ent_ry = Entry(self.popup, width=6)
        self.ent_ry.grid(row=3, column=1)
        self.ent_ry.insert(0, "300")

        Button(self.popup, text="Draw", command=self.get_input).grid(row=4, column=0, columnspan=2, pady=10)

    def get_input(self):
        try:
            self.xc = float(self.ent_xc.get())
            self.yc = float(self.ent_yc.get())
            self.rx = float(self.ent_rx.get())
            self.ry = float(self.ent_ry.get())
            self.popup.destroy()
        except ValueError:
            print("Valores inválidos")