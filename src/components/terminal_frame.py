from tkinter import *
from tkinter import font as tkfont

from services.log_service import LogService


class TerminalFrame(Frame):
    """Painel-terminal que exibe logs didáticos dos cálculos de CG."""
    RESIZE_HANDLE_HEIGHT = 6

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

    def __init__(
        self,
        master,
        on_toggle_minimize=None,
        on_resize_start=None,
        **kwargs,
    ):
        super().__init__(master, bg=self.BG, **kwargs)
        self._on_toggle_minimize = on_toggle_minimize
        self._on_resize_start = on_resize_start
        self._is_collapsed = False
        self._resize_enabled = False
        self._build_ui()
        self._register()

    def _build_ui(self):
        self.resize_handle = Frame(
            self,
            bg="#bdbdbd",
            height=self.RESIZE_HANDLE_HEIGHT,
            cursor="sb_v_double_arrow",
        )
        self.resize_handle.pack(side=TOP, fill=X)
        self.resize_handle.pack_propagate(False)
        self.resize_handle.bind("<ButtonPress-1>", self._start_resize)

        # ── Barra de título ─────────────────────────────────
        self.topbar = Frame(self, bg="#e0e0e0", height=28)
        self.topbar.pack(side=TOP, fill=X)
        self.topbar.pack_propagate(False)

        Label(
            self.topbar, text="● Terminal de Logs", fg="#000000",
            bg="#e0e0e0", font=("Segoe UI", 9, "bold"), anchor="w"
        ).pack(side=LEFT, padx=8)

        self.clear_button = Button(
            self.topbar, text="Limpar", fg="#000000", bg="#cccccc",
            activebackground="#aaaaaa", activeforeground="#000000",
            bd=0, padx=8, pady=1, font=("Segoe UI", 8),
            command=self._clear
        )
        self.clear_button.pack(side=RIGHT, padx=6, pady=3)

        self.toggle_button = Button(
            self.topbar, text="Minimizar", fg="#000000", bg="#cccccc",
            activebackground="#aaaaaa", activeforeground="#000000",
            bd=0, padx=8, pady=1, font=("Segoe UI", 8),
            command=self._toggle_minimize
        )
        self.toggle_button.pack(side=RIGHT, padx=0, pady=3)

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

    def set_collapsed(self, collapsed: bool):
        if self._is_collapsed == collapsed:
            return

        self._is_collapsed = collapsed
        if collapsed:
            self.text_frame.pack_forget()
            return

        self.text_frame.pack(side=TOP, fill=BOTH, expand=True)

    def set_resizable(self, enabled: bool):
        if self._resize_enabled == enabled:
            return

        self._resize_enabled = enabled
        if enabled:
            self.resize_handle.configure(cursor="sb_v_double_arrow")
            self.resize_handle.pack(side=TOP, fill=X, before=self.topbar)
            return

        self.resize_handle.pack_forget()

    def set_view_state(self, is_minimized: bool):
        self.toggle_button.configure(
            text="Expandir" if is_minimized else "Minimizar"
        )

    def _toggle_minimize(self):
        if callable(self._on_toggle_minimize):
            self._on_toggle_minimize()

    def _start_resize(self, event):
        if not self._resize_enabled:
            return

        if callable(self._on_resize_start):
            self._on_resize_start(event)

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
