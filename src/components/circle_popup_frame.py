from tkinter import * 

from src.components.shared.popup_frame import PopupFrame

class CircleFrame(PopupFrame):
    def __init__(self, root, **kwargs):
       super().__init__(root, **kwargs)

    def open_popup(self):
        Label(self.popup, text="Radian").grid(row=0, column=0, pady=5)
        self.radian = Entry(self.popup, width=6)
        self.radian.grid(row=0, column=1)

        btn = Button(self.popup, text="Drow", command=self.get_input)
        btn.grid(row=2, column=0, columnspan=3, pady=12)

        # Centralizar colunas
        self.popup.grid_columnconfigure(0, weight=1)
        self.popup.grid_columnconfigure(1, weight=1)
        self.popup.grid_columnconfigure(2, weight=1)

    def get_input(self):
        try:
            self.radian = float(self.radian.get())

            self.popup.destroy()
        except ValueError:
            print("Valores Invalidos")

        