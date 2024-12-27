import tkinter as tk
from tkinter import ttk
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def buscar_informacoes_enfermaria():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT nome_produto, quantidade, tipo_produto
                    FROM estoque
                    WHERE id_instituicao IS NOT NULL
                """
                cursor.execute(query)
                return cursor.fetchall()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao buscar informações da enfermaria: {e}")
        return []

def pagina_informacoes_enfermaria(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    informacoes = buscar_informacoes_enfermaria()
    texto_informacoes = "\n".join([f"Produto: {nome} - Quantidade: {quantidade} - Tipo: {tipo}" for nome, quantidade, tipo in informacoes])

    tk.Label(frame, text="Informações da Enfermaria:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    tk.Label(frame, text=texto_informacoes, font=FONT, justify="left").grid(row=1, column=0, padx=20, pady=10)

    tk.Button(frame, text="Fechar", font=FONT, command=parent.quit).grid(row=2, column=0, padx=20, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_informacoes_enfermaria(root)
    root.mainloop()
