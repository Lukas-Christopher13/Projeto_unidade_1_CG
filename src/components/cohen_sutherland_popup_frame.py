from tkinter import *
from tkinter import messagebox

from src.components.shared.popup_frame import PopupFrame


class CohenSutherlandClipFrame(PopupFrame):
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.draw_rectangle = False
        self.draw_line = False
        self.clip_line = False

        self.x1 = 100
        self.y1 = 100
        self.x2 = 400
        self.y2 = 300

        self.xmin = 200
        self.ymin = 200
        self.xmax = 400
        self.ymax = 350

        self.original_line = None
        self.clipped_result = None

    def open_popup(self):
        self.popup.protocol("WM_DELETE_WINDOW", self.popup.destroy)

        control_panel = Frame(self.popup)
        control_panel.pack(side=TOP, fill=X, padx=8, pady=8)

        Label(control_panel, text="Linha: x1").grid(row=0, column=0, padx=2, pady=2)
        self.txt_x1 = Entry(control_panel, width=6)
        self.txt_x1.grid(row=0, column=1, padx=2, pady=2)
        self.txt_x1.insert(0, "100")

        Label(control_panel, text="y1").grid(row=0, column=2, padx=2, pady=2)
        self.txt_y1 = Entry(control_panel, width=6)
        self.txt_y1.grid(row=0, column=3, padx=2, pady=2)
        self.txt_y1.insert(0, "100")

        Label(control_panel, text="x2").grid(row=0, column=4, padx=2, pady=2)
        self.txt_x2 = Entry(control_panel, width=6)
        self.txt_x2.grid(row=0, column=5, padx=2, pady=2)
        self.txt_x2.insert(0, "400")

        Label(control_panel, text="y2").grid(row=0, column=6, padx=2, pady=2)
        self.txt_y2 = Entry(control_panel, width=6)
        self.txt_y2.grid(row=0, column=7, padx=2, pady=2)
        self.txt_y2.insert(0, "300")

        Label(control_panel, text="Janela: xmin").grid(row=1, column=0, padx=2, pady=2)
        self.txt_xmin = Entry(control_panel, width=6)
        self.txt_xmin.grid(row=1, column=1, padx=2, pady=2)
        self.txt_xmin.insert(0, "200")

        Label(control_panel, text="ymin").grid(row=1, column=2, padx=2, pady=2)
        self.txt_ymin = Entry(control_panel, width=6)
        self.txt_ymin.grid(row=1, column=3, padx=2, pady=2)
        self.txt_ymin.insert(0, "200")

        Label(control_panel, text="Largura").grid(row=1, column=4, padx=2, pady=2)
        self.txt_width = Entry(control_panel, width=6)
        self.txt_width.grid(row=1, column=5, padx=2, pady=2)
        self.txt_width.insert(0, "200")

        Label(control_panel, text="Altura").grid(row=1, column=6, padx=2, pady=2)
        self.txt_height = Entry(control_panel, width=6)
        self.txt_height.grid(row=1, column=7, padx=2, pady=2)
        self.txt_height.insert(0, "150")

        Button(control_panel, text="Desenhar Janela", command=self._on_draw_rectangle).grid(row=2, column=0, columnspan=2, padx=3, pady=6, sticky="ew")
        Button(control_panel, text="Desenhar Linha", command=self._on_draw_line).grid(row=2, column=2, columnspan=2, padx=3, pady=6, sticky="ew")
        Button(control_panel, text="Recortar Linha", command=self._on_clip_line).grid(row=2, column=4, columnspan=2, padx=3, pady=6, sticky="ew")
        Button(control_panel, text="Limpar Tela", command=self._on_clear).grid(row=2, column=6, columnspan=2, padx=3, pady=6, sticky="ew")

        self.canvas = Canvas(self.popup, bg="white", height=430)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True, padx=8)

        self.log_area = Text(self.popup, height=10, width=40)
        self.log_area.pack(side=BOTTOM, fill=X, padx=8, pady=(8, 8))
        self.log_area.configure(state=DISABLED)

    def _on_draw_rectangle(self):
        if not self._parse_rectangle_inputs():
            return

        self.draw_rectangle = True
        self.draw_line = False
        self.clip_line = False
        self.clipped_result = None

        self._append_log("Desenhando a janela de visao")
        self._redraw()

    def _on_draw_line(self):
        if not self._parse_line_inputs():
            return

        self.draw_line = True
        self.clip_line = False
        self.clipped_result = None

        self._append_log("Desenhando a linha original")
        self._redraw()

    def _on_clip_line(self):
        if not self._parse_rectangle_inputs():
            return
        if not self._parse_line_inputs():
            return

        self.draw_rectangle = True
        self.draw_line = False
        self.clip_line = True

        self._append_log("Aplicando o algoritmo de recorte Cohen-Sutherland")
        self.clipped_result = self._cohen_sutherland(self.x1, self.y1, self.x2, self.y2)

        if self.clipped_result is None:
            self._append_log("Linha completamente fora da janela de visao e rejeitada")

        self._redraw()

    def _on_clear(self):
        self.draw_rectangle = False
        self.draw_line = False
        self.clip_line = False
        self.clipped_result = None
        self.canvas.delete("all")
        self._append_log("Tela limpa")

    def _redraw(self):
        self.canvas.delete("all")

        if self.draw_rectangle:
            self.canvas.create_rectangle(self.xmin, self.ymin, self.xmax, self.ymax, outline="black", width=1)
            self._append_log(
                f"Janela de visao desenhada: ({self.xmin}, {self.ymin}) ate ({self.xmax}, {self.ymax})"
            )

        if self.draw_line:
            self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="red", width=1)
            self._append_log(
                f"Linha desenhada: ({self.x1}, {self.y1}) ate ({self.x2}, {self.y2})"
            )

        if self.clip_line and self.clipped_result is not None:
            cx1, cy1, cx2, cy2 = self.clipped_result
            self.canvas.create_line(cx1, cy1, cx2, cy2, fill="green", width=1)
            self._append_log(
                f"Linha recortada: ({cx1}, {cy1}) ate ({cx2}, {cy2})"
            )

    def _parse_line_inputs(self):
        try:
            self.x1 = int(self.txt_x1.get())
            self.y1 = int(self.txt_y1.get())
            self.x2 = int(self.txt_x2.get())
            self.y2 = int(self.txt_y2.get())
            return True
        except ValueError:
            messagebox.showerror("Erro", "Coordenadas da linha invalidas.")
            return False

    def _parse_rectangle_inputs(self):
        try:
            width = int(self.txt_width.get())
            height = int(self.txt_height.get())
            if width <= 0 or height <= 0:
                messagebox.showerror("Erro", "Largura e altura devem ser maiores que zero.")
                return False

            self.xmin = int(self.txt_xmin.get())
            self.ymin = int(self.txt_ymin.get())
            self.xmax = self.xmin + width
            self.ymax = self.ymin + height
            return True
        except ValueError:
            messagebox.showerror("Erro", "Valores da janela de recorte invalidos.")
            return False

    def _append_log(self, message):
        self.log_area.configure(state=NORMAL)
        self.log_area.insert(END, f"{message}\n")
        self.log_area.see(END)
        self.log_area.configure(state=DISABLED)

    def _compute_out_code(self, x, y):
        code = 0

        if y > self.ymax:
            code |= self.TOP
        elif y < self.ymin:
            code |= self.BOTTOM

        if x > self.xmax:
            code |= self.RIGHT
        elif x < self.xmin:
            code |= self.LEFT

        return code

    def _cohen_sutherland(self, x1, y1, x2, y2):
        code1 = self._compute_out_code(x1, y1)
        code2 = self._compute_out_code(x2, y2)
        self._append_log(f"Codigo inicial - P1: {code1:04b}, P2: {code2:04b}")

        while True:
            if (code1 | code2) == 0:
                return [int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))]

            if (code1 & code2) != 0:
                return None

            out_code = code1 if code1 != 0 else code2
            x = 0.0
            y = 0.0

            if (out_code & self.TOP) != 0:
                if y2 == y1:
                    return None
                x = x1 + (x2 - x1) * (self.ymax - y1) / (y2 - y1)
                y = self.ymax
                self._append_log(f"Intersecao com linha superior em ({int(round(x))}, {int(round(y))})")

            elif (out_code & self.BOTTOM) != 0:
                if y2 == y1:
                    return None
                x = x1 + (x2 - x1) * (self.ymin - y1) / (y2 - y1)
                y = self.ymin
                self._append_log(f"Intersecao com linha inferior em ({int(round(x))}, {int(round(y))})")

            elif (out_code & self.RIGHT) != 0:
                if x2 == x1:
                    return None
                y = y1 + (y2 - y1) * (self.xmax - x1) / (x2 - x1)
                x = self.xmax
                self._append_log(f"Intersecao com linha direita em ({int(round(x))}, {int(round(y))})")

            elif (out_code & self.LEFT) != 0:
                if x2 == x1:
                    return None
                y = y1 + (y2 - y1) * (self.xmin - x1) / (x2 - x1)
                x = self.xmin
                self._append_log(f"Intersecao com linha esquerda em ({int(round(x))}, {int(round(y))})")

            if out_code == code1:
                x1 = x
                y1 = y
                code1 = self._compute_out_code(x1, y1)
            else:
                x2 = x
                y2 = y
                code2 = self._compute_out_code(x2, y2)

            self._append_log(f"Novo codigo - P1: {code1:04b}, P2: {code2:04b}")

    def get_input(self):
        # Interface mantida por compatibilidade com PopupFrame.
        return None
