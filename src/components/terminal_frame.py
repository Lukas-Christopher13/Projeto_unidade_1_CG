from tkinter import *
from tkinter import font as tkfont

from services.log_service import LogService


class TerminalFrame(Frame):
    """Painel-terminal que exibe logs didáticos dos cálculos de CG."""

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
        self._build_ui()
        self._register()

    def _build_ui(self):
        # ── Barra de título ─────────────────────────────────
        topbar = Frame(self, bg="#e0e0e0", height=28)
        topbar.pack(side=TOP, fill=X)
        topbar.pack_propagate(False)

        Label(
            topbar, text="● Terminal de Logs", fg="#000000",
            bg="#e0e0e0", font=("Segoe UI", 9, "bold"), anchor="w"
        ).pack(side=LEFT, padx=8)

        Button(
            topbar, text="Limpar", fg="#000000", bg="#cccccc",
            activebackground="#aaaaaa", activeforeground="#000000",
            bd=0, padx=8, pady=1, font=("Segoe UI", 8),
            command=self._clear
        ).pack(side=RIGHT, padx=6, pady=3)

        # ── Área de texto ───────────────────────────────────
        text_frame = Frame(self, bg=self.BG)
        text_frame.pack(side=TOP, fill=BOTH, expand=True)

        mono = tkfont.Font(family="Consolas", size=10)

        self.text = Text(
            text_frame, bg=self.BG, fg=self.FG,
            font=mono, wrap=WORD, bd=0,
            padx=10, pady=8,
            state=DISABLED, cursor="arrow",
            insertbackground=self.FG,
            selectbackground="#cccccc",
            selectforeground="#000000",
        )

        scrollbar = Scrollbar(
            text_frame, orient=VERTICAL, command=self.text.yview,
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
