from tkinter import * 

class LineFrame(Frame):
    def __init__(self, root, **kwargs):
       self.root = root

    def open_popup(self):
        self.popup = Toplevel(self.root)
        self.popup.title("Line")
        
        w = 400
        h = 150
        self.popup.geometry(f"{w}x{h}")

        #Centraliza o self.popup
        self.popup.update_idletasks()  
        sw = self.popup.winfo_screenwidth()
        sh = self.popup.winfo_screenheight()

        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.popup.geometry(f"{w}x{h}+{x}+{y}")

        Label(self.popup, text="Ponto A (x1, y1):").grid(row=0, column=0, pady=5)
        self.ent_x1 = Entry(self.popup, width=6)
        self.ent_y1 = Entry(self.popup, width=6)
        self.ent_x1.grid(row=0, column=1)
        self.ent_y1.grid(row=0, column=2)

        Label(self.popup, text="Ponto B (x2, y2):").grid(row=1, column=0, pady=5)
        self.ent_x2 = Entry(self.popup, width=6)
        self.ent_y2 = Entry(self.popup, width=6)
        self.ent_x2.grid(row=1, column=1)
        self.ent_y2.grid(row=1, column=2)

        btn = Button(self.popup, text="Desenhar", command=self.get_input)
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

        