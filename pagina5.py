import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def mostrar_ids(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame)
    canvas.pack(side="left", fill="both", expand=True)

    h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
    h_scrollbar.pack(side="bottom", fill="x")

    v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    v_scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)

    # IDs de Usuários
    ttk.Label(scrollable_frame, text="IDs de Usuários:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario, nome FROM usuarios")
                usuarios = cursor.fetchall()
                texto_usuarios = "\n".join([f"{id_usuario}: {nome}" for id_usuario, nome in usuarios])
                ttk.Label(scrollable_frame, text=texto_usuarios, font=FONT, justify="left").grid(row=1, column=0, padx=20, pady=10, sticky="w")
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao buscar IDs de usuários: {e}")

    # IDs de Instituições
    ttk.Label(scrollable_frame, text="IDs de Instituições:", font=FONT).grid(row=0, column=1, padx=20, pady=10, sticky="e")
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_instituicao, nome FROM instituicao")
                instituicoes = cursor.fetchall()
                texto_instituicoes = "\n".join([f"{id_instituicao}: {nome}" for id_instituicao, nome in instituicoes])
                ttk.Label(scrollable_frame, text=texto_instituicoes, font=FONT, justify="left").grid(row=1, column=1, padx=20, pady=10, sticky="w")
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao buscar IDs de instituições: {e}")

    # IDs de Enfermarias
    ttk.Label(scrollable_frame, text="IDs de Enfermarias:", font=FONT).grid(row=0, column=2, padx=20, pady=10, sticky="e")
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_enfermaria, medicamento FROM enfermaria")
                enfermarias = cursor.fetchall()
                texto_enfermarias = "\n".join([f"{id_enfermaria}: {medicamento}" for id_enfermaria, medicamento in enfermarias])
                ttk.Label(scrollable_frame, text=texto_enfermarias, font=FONT, justify="left").grid(row=1, column=2, padx=20, pady=10, sticky="w")
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao buscar IDs de enfermarias: {e}")

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    mostrar_ids(root)
    root.mainloop()
