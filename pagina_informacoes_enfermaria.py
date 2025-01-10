import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def buscar_informacoes_enfermaria():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        e.id_enfermaria, e.nome, i.nome AS nome_instituicao
                    FROM enfermaria e
                    JOIN instituicao i ON e.id_instituicao = i.id_instituicao
                """
                cursor.execute(query)
                resultados = cursor.fetchall()
                
                if resultados:
                    informacoes = ""
                    for linha in resultados:
                        informacoes += f"ID Enfermaria: {linha[0]}\n"
                        informacoes += f"Nome da Enfermaria: {linha[1]}\n"
                        informacoes += f"Instituição: {linha[2]}\n\n"
                    return informacoes
                else:
                    return "Nenhuma informação encontrada."
    except cx_Oracle.DatabaseError as e:
        return f"Erro ao buscar informações: {e}"

def pagina_informacoes_enfermaria(parent):
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

    ttk.Label(scrollable_frame, text="Informações da Enfermaria", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="w")

    def exibir_informacoes():
        informacoes = buscar_informacoes_enfermaria()
        label_informacoes.config(text=informacoes)

    label_informacoes = ttk.Label(scrollable_frame, text="", font=FONT, justify="left")
    label_informacoes.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    ttk.Button(scrollable_frame, text="Buscar Informações", command=exibir_informacoes).grid(row=2, column=0, padx=20, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_informacoes_enfermaria(root)
    root.deiconify()  # Mostrar a janela principal
    root.mainloop()
