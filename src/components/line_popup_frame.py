from tkinter import * 

from src.components.shared.popup_frame import PopupFrame

class LineFrame(PopupFrame):
    def __init__(self, root, **kwargs):
       super().__init__(root, **kwargs)

    def open_popup(self):
        Label(self.popup, text="Point A (x1, y1):").grid(row=0, column=0, pady=5)
        self.ent_x1 = Entry(self.popup, width=6)
        self.ent_y1 = Entry(self.popup, width=6)
        self.ent_x1.grid(row=0, column=1)
        self.ent_y1.grid(row=0, column=2)

        Label(self.popup, text="Point B (x2, y2):").grid(row=1, column=0, pady=5)
        self.ent_x2 = Entry(self.popup, width=6)
        self.ent_y2 = Entry(self.popup, width=6)
        self.ent_x2.grid(row=1, column=1)
        self.ent_y2.grid(row=1, column=2)

        btn = Button(self.popup, text="Drow", command=self.get_input)
        btn.grid(row=2, column=0, columnspan=3, pady=12)

        # Centralizar colunas
        self.popup.grid_columnconfigure(0, weight=1)
        self.popup.grid_columnconfigure(1, weight=1)
        self.popup.grid_columnconfigure(2, weight=1)

    def get_input(self):
        try:
            self.x1 = float(self.ent_x1.get())
            self.y1 = float(self.ent_y1.get())
            self.x2 = float(self.ent_x2.get())
            self.y2 = float(self.ent_y2.get())
            
            self.popup.destroy()

        except ValueError:
            print("Valores Invalidos")

        