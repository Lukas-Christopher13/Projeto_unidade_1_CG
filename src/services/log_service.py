import numpy as np


class LogService:
    """Singleton que acumula logs e notifica listeners (TerminalFrame)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._listeners = []
        return cls._instance

    # ── logging ──────────────────────────────────────

    def header(self, text: str):
        """Título da operação. Ex: ═══ RETA DDA ═══"""
        line = f"\n{'═' * 3} {text} {'═' * 3}"
        self._emit("header", line)

    def step(self, text: str):
        """Passo intermediário. Ex: 1. Δx = 10"""
        self._emit("step", f"  {text}")

    def result(self, text: str):
        """Resultado final. Ex: → Pixel(3, 7)"""
        self._emit("result", f"  → {text}")

    def separator(self):
        """Linha em branco."""
        self._emit("step", "")

    def matrix(self, label: str, mat):
        """Exibe uma matriz 4x4 formatada."""
        self._emit("matrix_label", f"  {label}:")
        if isinstance(mat, np.ndarray):
            for row in mat:
                formatted = "  │ " + "  ".join(f"{v:>8.2f}" for v in row) + " │"
                self._emit("matrix", formatted)
        self._emit("step", "")

    def info(self, text: str):
        """Informação complementar."""
        self._emit("info", f"  {text}")

    def iteration(self, text: str):
        """Iteração de algoritmo. Ex: k=0: x=1.0 y=2.0 → Pixel(1, 2)"""
        self._emit("iteration", f"    {text}")

    # ── Padrão Observer ────────────────────────────────────

    def add_listener(self, callback):
        self._listeners.append(callback)

    def remove_listener(self, callback):
        self._listeners.remove(callback)

    def clear(self):
        for cb in self._listeners:
            cb("clear", "")

    # ── Interno ─────────────────────────────────────────────

    def _emit(self, tag: str, text: str):
        for cb in self._listeners:
            cb(tag, text)
