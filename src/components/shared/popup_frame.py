from tkinter import * 

from abc import ABC, abstractmethod


class PopupFrame(ABC, Frame):
    w = 400
    h = 150

    def __init__(self, root, **kwargs):
        self.root = root
        self.popup = Toplevel(self.root)
        self.popup.title("Line")
        self.popup.geometry(f"{self.w}x{self.h}")
 
        self.popup.update_idletasks()  
        sw = self.popup.winfo_screenwidth()
        sh = self.popup.winfo_screenheight()

        x = (sw // 2) - (self.w // 2)
        y = (sh // 2) - (self.h // 2)
        self.popup.geometry(f"{self.w}x{self.h}+{x}+{y}")

    @abstractmethod
    def open_popup(self):
        pass

    @abstractmethod
    def get_input(self):
       pass

        