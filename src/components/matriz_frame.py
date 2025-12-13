from tkinter import *

from src.utils.array_util import transpose
from src.components.shared.popup_frame import PopupFrame


TITLE = "Add Points"
WIDITH = 800
HEIGHT = 800

class MatrizFrame(PopupFrame):
    def __init__(self, root):
        super().__init__(
            root, 
            title=TITLE,  
            w=WIDITH, 
            h=HEIGHT
        )
        self.root = root

    def open_popup(self):
        self.grid = []
        self.input = []
        
        # Tamanho inicial da matriz (2x2)
        self.rows = 3
        self.cols = 3

        # Frame para a matriz
        self.frame = Frame(self.popup)
        self.frame.pack()

        # Função para criar os campos da matriz
        self.create_matrix()

        self.add_col_button = Button(self.popup, text="Adicionar Coluna", command=self.add_column)
        self.add_col_button.pack()

        self.finish_button = Button(self.popup, text="Finish", command=self.get_input)
        self.finish_button.pack()

    def get_input(self):
        for line in self.grid:
            line_values = []
            for entry in line:
                value = entry.get()
                line_values.append(float(value) if value else 0.0)
            self.input.append(line_values)

        self.input = transpose(self.input)
        self.popup.destroy()

    def create_matrix(self):
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                entry = Entry(self.frame, width=5)
                entry.grid(row=r, column=c)
                row.append(entry)
            self.grid.append(row)

    def add_column(self):
        self.cols += 1
        for r in range(self.rows):
            entry = Entry(self.frame, width=5)
            entry.grid(row=r, column=self.cols-1)
            self.grid[r].append(entry)

    