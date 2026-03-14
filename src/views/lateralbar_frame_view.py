from tkinter import *
from tkinter import ttk
from src.models.gl_window_model import gl_window_model
from src.views.edit_shape_view import EditShapeView 

class LateralBarView(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        gl_window_model.add_frame(self)
        self.columnconfigure(0, weight=1)

        self.transform_container = Frame(self)
        self.transform_container.grid(row=0, column=0, sticky="nsew")
        self.transform_container.columnconfigure(0, weight=1)
        self.transform_container.columnconfigure(1, weight=0)

        self.points_title = ttk.Label(self.transform_container, text="Pontos")
        self.points_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.listbox = Listbox(self.transform_container)
        self.listbox.grid(row=1, column=0, sticky="ew")

        self.scrollbar = Scrollbar(self.transform_container, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.point_form = ttk.LabelFrame(self.transform_container, text="Adicionar ponto", padding=(8, 8))
        self.point_form.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 8))

        self._on_add_point = None
        self._build_point_form()

        self.edit_shape_view = EditShapeView(self.transform_container)
        self.edit_shape_view.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        self.algorithm_container = ttk.LabelFrame(self, text="Algoritmo", padding=(10, 8))
        self.algorithm_container.columnconfigure(0, weight=1)

        self.algorithm_title = ttk.Label(self.algorithm_container, text="Selecione um algoritmo na barra superior")
        self.algorithm_title.grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.algorithm_form = Frame(self.algorithm_container)
        self.algorithm_form.grid(row=1, column=0, sticky="ew")

        self.apply_button = ttk.Button(self.algorithm_container, text="Executar")
        self.apply_button.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        self._line_inputs = {}
        self._circle_inputs = {}

        self.show_transform_screen()

    def _build_point_form(self):
        for widget in self.point_form.winfo_children():
            widget.destroy()

        if gl_window_model.is_2d():
            self.points_title.configure(text="Pontos do plano (X, Y)")
        else:
            self.points_title.configure(text="Pontos do espaco (X, Y, Z)")

        self.point_form.columnconfigure(0, weight=1)
        self.point_form.columnconfigure(1, weight=1)
        self.point_form.columnconfigure(2, weight=1)

        ttk.Label(self.point_form, text="X").grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.point_x = ttk.Entry(self.point_form, width=10)
        self.point_x.grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=(0, 2))
        self.point_x.insert(0, "0.0")

        ttk.Label(self.point_form, text="Y").grid(row=0, column=1, sticky="w", pady=(0, 2))
        self.point_y = ttk.Entry(self.point_form, width=10)
        self.point_y.grid(row=1, column=1, sticky="ew", padx=4, pady=(0, 2))
        self.point_y.insert(0, "0.0")

        self.point_z = None
        row_btn = 2
        if not gl_window_model.is_2d():
            ttk.Label(self.point_form, text="Z").grid(row=0, column=2, sticky="w", pady=(0, 2))
            self.point_z = ttk.Entry(self.point_form, width=10)
            self.point_z.grid(row=1, column=2, sticky="ew", padx=(4, 0), pady=(0, 2))
            self.point_z.insert(0, "0.0")

        self.add_point_btn = ttk.Button(self.point_form, text="Adicionar ponto")
        self.add_point_btn.grid(row=row_btn, column=0, columnspan=3, sticky="ew", pady=(8, 2))

        if self._on_add_point is not None:
            self.add_point_btn.configure(command=self._on_add_point)

    def rebuild(self):
        self._build_point_form()

    def show_transform_screen(self):
        self.algorithm_container.grid_remove()
        self.transform_container.grid(row=0, column=0, sticky="nsew")

    def show_line_algorithm_screen(self, title: str):
        self._show_algorithm_shell(f"Linha - {title}")
        self._clear_algorithm_form()

        self._line_inputs["x1"] = self._add_number_input(0, "x1", "0.0")
        self._line_inputs["y1"] = self._add_number_input(1, "y1", "0.0")
        self._line_inputs["x2"] = self._add_number_input(2, "x2", "10.0")
        self._line_inputs["y2"] = self._add_number_input(3, "y2", "10.0")

    def show_circle_algorithm_screen(self, title: str):
        self._show_algorithm_shell(f"Circulo - {title}")
        self._clear_algorithm_form()

        self._circle_inputs["radian"] = self._add_number_input(0, "Raio", "30.0")
        self._circle_inputs["origin_x"] = self._add_number_input(1, "Origem X", "0.0")
        self._circle_inputs["origin_y"] = self._add_number_input(2, "Origem Y", "0.0")

    def get_line_inputs(self):
        try:
            return {
                "x1": float(self._line_inputs["x1"].get()),
                "y1": float(self._line_inputs["y1"].get()),
                "x2": float(self._line_inputs["x2"].get()),
                "y2": float(self._line_inputs["y2"].get()),
            }
        except (ValueError, KeyError):
            return None

    def get_circle_inputs(self):
        try:
            return {
                "radian": float(self._circle_inputs["radian"].get()),
                "origin_x": float(self._circle_inputs["origin_x"].get()),
                "origin_y": float(self._circle_inputs["origin_y"].get()),
            }
        except (ValueError, KeyError):
            return None

    def set_algorithm_action(self, text: str, command):
        self.apply_button.configure(text=text, command=command)

    def set_point_actions(self, on_add_point):
        self._on_add_point = on_add_point
        self.add_point_btn.configure(command=on_add_point)

    def get_point_input(self):
        try:
            x = float(self.point_x.get())
            y = float(self.point_y.get())
            z = 0.0 if self.point_z is None else float(self.point_z.get())
            return [x, y, z]
        except ValueError:
            return None

    def set_points(self, points):
        self.listbox.delete(0, "end")
        for idx, p in enumerate(points):
            self.listbox.insert("end", f"P{idx}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})")

    def _show_algorithm_shell(self, title: str):
        self.transform_container.grid_remove()
        self.algorithm_title.configure(text=title)
        self.algorithm_container.grid(row=0, column=0, sticky="nsew")

    def _clear_algorithm_form(self):
        for widget in self.algorithm_form.winfo_children():
            widget.destroy()

        self._line_inputs = {}
        self._circle_inputs = {}

    def _add_number_input(self, row: int, label: str, default: str):
        ttk.Label(self.algorithm_form, text=label).grid(row=row, column=0, sticky="w", pady=2)
        entry = ttk.Entry(self.algorithm_form, width=12)
        entry.grid(row=row, column=1, sticky="ew", padx=(8, 0), pady=2)
        entry.insert(0, default)
        return entry
        

  
    