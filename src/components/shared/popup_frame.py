from tkinter import * 

from abc import ABC, abstractmethod


class PopupFrame(ABC, Frame):
    def __init__(self, root, title="",  w=400, h=150,  **kwargs):
        self.title = title
        self.w = w
        self.h = h
        self.root = root
        self.popup = Toplevel(self.root)
        self.popup.title(title)
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
