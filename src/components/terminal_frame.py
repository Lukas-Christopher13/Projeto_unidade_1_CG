from tkinter import *
from tkinter import font as tkfont

from services.log_service import LogService


class TerminalFrame(Frame):
    """Painel-terminal que exibe logs didáticos dos cálculos de CG."""
    TOPBAR_HEIGHT = 28
    RESIZE_HANDLE_HEIGHT = 6
    EXPANDED_RATIO = 0.30
    MIN_EXPANDED_HEIGHT = 96
    HANDLE_COLOR = "#d9d9d9"

    # Esquema de cores (preto e branco)
    BG = "#ffffff"
    FG = "#000000"
    COLORS = {
        "header":       "#000000",
        "step":         "#000000",
        "result":       "#000000",
        "matrix_label": "#000000",
        "matrix":       "#000000",
        "info":         "#333333",
        "iteration":    "#333333",
    }

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=self.BG, **kwargs)
        self.host = None
        self.collapsed = False
        self.preferred_height = None
        self._build_ui()
        self._register()

    def _build_ui(self):
        self.resize_handle = Frame(
            self,
            bg=self.HANDLE_COLOR,
            height=self.RESIZE_HANDLE_HEIGHT,
            cursor="sb_v_double_arrow",
        )
        self.resize_handle.pack(side=TOP, fill=X)
        self.resize_handle.pack_propagate(False)

        # ── Barra de título ─────────────────────────────────
        self.topbar = Frame(self, bg="#e0e0e0", height=self.TOPBAR_HEIGHT)
        self.topbar.pack(side=TOP, fill=X)
        self.topbar.pack_propagate(False)

        self.title_label = Label(
            self.topbar, text="● Terminal de Logs", fg="#000000",
            bg="#e0e0e0", font=("Segoe UI", 9, "bold"), anchor="w"
        )
        self.title_label.pack(side=LEFT, padx=8)

        self.toggle_button = Button(
            self.topbar, text="Minimizar", fg="#000000", bg="#cccccc",
            activebackground="#aaaaaa", activeforeground="#000000",
            bd=0, padx=8, pady=1, font=("Segoe UI", 8),
            command=self.toggle
        )
        self.toggle_button.pack(side=RIGHT, padx=(0, 6), pady=3)

        self.clear_button = Button(
            self.topbar, text="Limpar", fg="#000000", bg="#cccccc",
            activebackground="#aaaaaa", activeforeground="#000000",
            bd=0, padx=8, pady=1, font=("Segoe UI", 8),
            command=self._clear
        )
        self.clear_button.pack(side=RIGHT, padx=6, pady=3)

        # ── Área de texto ───────────────────────────────────
        self.text_frame = Frame(self, bg=self.BG)
        self.text_frame.pack(side=TOP, fill=BOTH, expand=True)

        mono = tkfont.Font(family="Consolas", size=10)

        self.text = Text(
            self.text_frame, bg=self.BG, fg=self.FG,
            font=mono, wrap=WORD, bd=0,
            padx=10, pady=8,
            state=DISABLED, cursor="arrow",
            insertbackground=self.FG,
            selectbackground="#cccccc",
            selectforeground="#000000",
        )

        scrollbar = Scrollbar(
            self.text_frame, orient=VERTICAL, command=self.text.yview,
            bg="#cccccc", troughcolor="#e0e0e0",
            activebackground="#aaaaaa",
        )
        self.text.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, fill=BOTH, expand=True)

        # ── Tags de cor ─────────────────────────────────────
        for tag, color in self.COLORS.items():
            bold = "bold" if tag == "header" else "normal"
            size = 11 if tag == "header" else 10
            self.text.tag_configure(
                tag,
                foreground=color,
                font=tkfont.Font(family="Consolas", size=size, weight=bold)
            )

        self.resize_handle.bind("<ButtonPress-1>", self._start_resize)
        self.resize_handle.bind("<B1-Motion>", self._perform_resize)
        self.resize_handle.bind("<ButtonRelease-1>", self._finish_resize)

    def attach_overlay(self, host):
        self.host = host
        self.place(in_=host, relx=0.0, rely=1.0, anchor="sw", relwidth=1.0)
        self.lift()
        self.update_layout()
        host.bind("<Configure>", self._on_host_configure, add="+")

    def update_layout(self):
        if self.host is None:
            return

        host_height = max(self.host.winfo_height(), self.TOPBAR_HEIGHT)
        overlay_height = self.calculate_overlay_height(
            host_height=host_height,
            collapsed=self.collapsed,
            preferred_height=self.preferred_height,
        )

        self.place_configure(height=overlay_height)
        self.lift()
        self._sync_text_visibility()
        self._sync_controls()

    def toggle(self):
        self.collapsed = not self.collapsed
        self.update_layout()

    def _sync_text_visibility(self):
        if self.collapsed:
            if self.resize_handle.winfo_manager():
                self.resize_handle.pack_forget()
        elif not self.resize_handle.winfo_manager():
            self.resize_handle.pack(side=TOP, fill=X, before=self.topbar)

        if self.collapsed:
            self.text_frame.pack_forget()
        elif not self.text_frame.winfo_manager():
            self.text_frame.pack(side=TOP, fill=BOTH, expand=True)

    def _sync_controls(self):
        self.toggle_button.config(text="Maximizar" if self.collapsed else "Minimizar")

    def _on_host_configure(self, event=None):
        self.update_layout()

    def _start_resize(self, event):
        if self.collapsed or self.host is None:
            return
        self._perform_resize(event)

    def _perform_resize(self, event):
        if self.collapsed or self.host is None:
            return

        host_bottom = self.host.winfo_rooty() + self.host.winfo_height()
        new_height = host_bottom - event.y_root
        self.preferred_height = new_height
        self.update_layout()

    def _finish_resize(self, event):
        if self.collapsed or self.host is None:
            return
        self._perform_resize(event)

    @classmethod
    def calculate_overlay_height(cls, host_height, collapsed, preferred_height=None):
        if collapsed:
            return cls.TOPBAR_HEIGHT

        desired_height = preferred_height
        if desired_height is None:
            desired_height = int(host_height * cls.EXPANDED_RATIO)

        min_height = cls.TOPBAR_HEIGHT + cls.RESIZE_HANDLE_HEIGHT + cls.MIN_EXPANDED_HEIGHT
        desired_height = max(min_height, desired_height)
        desired_height = min(host_height, desired_height)

        return desired_height

    def _register(self):
        """Registra como listener do LogService."""
        self.log = LogService()
        self.log.add_listener(self._on_log)

    def _on_log(self, tag: str, text: str):
        """Chamado pelo LogService quando há novo log."""
        if tag == "clear":
            self._clear()
            return

        self.text.config(state=NORMAL)
        self.text.insert(END, text + "\n", tag)
        self.text.config(state=DISABLED)
        self.text.see(END)

    def _clear(self):
        self.text.config(state=NORMAL)
        self.text.delete("1.0", END)
        self.text.config(state=DISABLED)
