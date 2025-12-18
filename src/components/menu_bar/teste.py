import tkinter as tk
from tkinter import messagebox

# Janela principal
root = tk.Tk()
root.title("Exemplo de Menu")
root.geometry("600x400")

# ===== MENU BAR =====
menu_bar = tk.Menu(root)

# ===== MENU FILE =====
menu_file = tk.Menu(menu_bar, tearoff=0)
menu_file.add_command(label="New", command=lambda: print("New"))
menu_file.add_command(label="Open", command=lambda: print("Open"))
menu_file.add_separator()
menu_file.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="File", menu=menu_file)

# ===== MENU EDIT =====
menu_edit = tk.Menu(menu_bar, tearoff=0)
menu_edit.add_command(label="Cut")
menu_edit.add_command(label="Copy")
menu_edit.add_command(label="Paste")

menu_bar.add_cascade(label="Edit", menu=menu_edit)

# ===== MENU HELP =====
menu_help = tk.Menu(menu_bar, tearoff=0)
menu_help.add_command(
    label="About",
    command=lambda: messagebox.showinfo("About", "Meu programa em Tkinter")
)

menu_bar.add_cascade(label="Help", menu=menu_help)

# Aplica o menu à janela
root.config(menu=menu_bar)

root.mainloop()
