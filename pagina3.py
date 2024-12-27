import tkinter as tk
from tkinter import ttk
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def cadastrar_produto_enfermaria(nome_produto, quantidade, tipo, id_enfermaria):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO estoque (nome_produto, quantidade, tipo_produto, id_instituicao)
                    VALUES (:1, :2, :3, :4)
                """
                cursor.execute(query, [nome_produto, quantidade, tipo, id_enfermaria])
                connection.commit()
                return True
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao cadastrar produto na enfermaria: {e}")
        return False

def pagina3(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Nome do Produto:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_nome_produto = tk.Entry(frame, width=30, font=FONT)
    entry_nome_produto.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(frame, text="Quantidade:", font=FONT).grid(row=1, column=0, padx=20, pady=10)
    entry_quantidade = tk.Entry(frame, width=30, font=FONT)
    entry_quantidade.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(frame, text="Tipo:", font=FONT).grid(row=2, column=0, padx=20, pady=10)
    entry_tipo = tk.Entry(frame, width=30, font=FONT)
    entry_tipo.grid(row=2, column=1, padx=20, pady=10)

    tk.Label(frame, text="ID da Enfermaria:", font=FONT).grid(row=3, column=0, padx=20, pady=10)
    entry_id_enfermaria = tk.Entry(frame, width=30, font=FONT)
    entry_id_enfermaria.grid(row=3, column=1, padx=20, pady=10)

    def cadastrar():
        nome_produto = entry_nome_produto.get()
        quantidade = entry_quantidade.get()
        tipo = entry_tipo.get()
        id_enfermaria = entry_id_enfermaria.get()

        if not cadastrar_produto_enfermaria(nome_produto, quantidade, tipo, id_enfermaria):
            print("Erro ao cadastrar produto na enfermaria.")
    
    tk.Button(frame, text="Cadastrar Produto", font=FONT, command=cadastrar).grid(row=4, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina3(root)
    root.mainloop()
