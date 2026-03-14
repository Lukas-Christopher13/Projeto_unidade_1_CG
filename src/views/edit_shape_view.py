from tkinter import *
from tkinter import ttk
from src.models.gl_window_model import gl_window_model

from src.views.inputs.scale_input_frame import ScaleInputFrame
from src.views.inputs.rotation_input_frame import RotationInputFrame
from src.views.inputs.translation_input_frame import TranslationInputFrame
from src.views.inputs.reflection_input_frame import ReflectionInputFrame
from src.views.inputs.share_input_frame import ShareInputFrame

class EditShapeView(Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self._configure_styles()

        self.columnconfigure(0, weight=1)
        gl_window_model.add_frame(self)

        self.rebuild()

    def rebuild(self):
        for widget in self.winfo_children():
            widget.destroy()

        title = ttk.Label(self, text="Painel de Transformacoes", style="PanelTitle.TLabel")
        title.grid(row=0, column=0, sticky="ew", padx=8, pady=(6, 8))

        row_idx = 1
        if not gl_window_model.is_2d():
            transforms_group = ttk.LabelFrame(self, text="Transformacoes", padding=(8, 8))
            transforms_group.grid(row=row_idx, column=0, sticky="ew", padx=8)
            transforms_group.columnconfigure(0, weight=1)

            self.translate_input_frame = TranslationInputFrame(
                transforms_group,
                title="Translate",
                command=self.translate,
                borderwidth=1,
                relief="flat"
            )
            self.translate_input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 6))

            self.rotation_input_frame = RotationInputFrame(
                transforms_group,
                title="Rotation",
                command=self.rotate,
                borderwidth=1,
                relief="flat"
            )
            self.rotation_input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 6))

            self.scaling_input_frame = ScaleInputFrame(
                transforms_group,
                title="Scaling",
                command=self.scale,
                borderwidth=1,
                relief="flat"
            )
            self.scaling_input_frame.grid(row=2, column=0, sticky="ew", pady=(0, 6))

            self.reflection_input_frame = ReflectionInputFrame(
                transforms_group,
                title="Reflection",
                command=self.reflection,
                borderwidth=1,
                relief="flat"
            )
            self.reflection_input_frame.grid(row=3, column=0, sticky="ew", pady=(0, 6))

            self.share_input_frame = ShareInputFrame(
                transforms_group,
                title="Share",
                command=self.share,
                borderwidth=1,
                relief="flat"
            )
            self.share_input_frame.grid(row=4, column=0, sticky="ew")

            row_idx += 1

        actions_group = ttk.LabelFrame(self, text="Acoes", padding=(8, 8))
        actions_group.grid(row=row_idx, column=0, sticky="ew", padx=8, pady=(8, 0))
        actions_group.columnconfigure(0, weight=1)
        actions_group.columnconfigure(1, weight=1)

        if not gl_window_model.is_2d():
            btn_to_origin = ttk.Button(actions_group, text="To Origin", command=self.to_origin)
            btn_to_origin.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=(0, 6))

            btn_delete = ttk.Button(actions_group, text="Delete Shape", command=self.delete)
            btn_delete.grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=(0, 6))

            row_clear = 1
        else:
            btn_comb = ttk.Button(actions_group, text="Comb. Transform", command=self.comb)
            btn_comb.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))

            row_clear = 1

        btn_clear_all = ttk.Button(actions_group, text="Limpar Tudo", command=self.clear_all)
        btn_clear_all.grid(row=row_clear, column=0, columnspan=2, sticky="ew")

    def _configure_styles(self):
        style = ttk.Style(self)
        style.configure("PanelTitle.TLabel", font=("Segoe UI", 10, "bold"))

    def set_controller(self, controller):
        self.controller = controller

    def rotate(self):
        self.controller.rotate()

    def translate(self):
        self.controller.translate()

    def scale(self):
        self.controller.scale()

    def transform(self):
        self.controller.transform()
        
    def to_origin(self):
        self.controller.to_origin()

    def delete(self):
        self.controller.delete()

    def comb(self):
        self.controller.comb()

    def reflection(self, reflection_type: str):
        self.controller.reflection(reflection_type)

    def share(self):
        self.controller.share()

    def clear_all(self):
        self.controller.clear_all()

    def do_not(self):
        pass
