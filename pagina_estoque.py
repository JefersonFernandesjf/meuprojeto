import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def cadastrar_produto_estoque(nome_produto, quantidade, tipo_produto, id_instituicao):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO estoque (nome_produto, quantidade, tipo_produto, id_instituicao)
                    VALUES (:1, :2, :3, :4)
                """
                cursor.execute(query, [nome_produto, quantidade, tipo_produto, id_instituicao])
                connection.commit()
                messagebox.showinfo("Sucesso", "Produto cadastrado no estoque com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar produto no estoque: {e}")
        return False

def pagina_estoque(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    tk.Label(scrollable_frame, text="Nome do Produto:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_nome_produto = tk.Entry(scrollable_frame, width=30, font=FONT)
    entry_nome_produto.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(scrollable_frame, text="Quantidade:", font=FONT).grid(row=1, column=0, padx=20, pady=10)
    entry_quantidade = tk.Entry(scrollable_frame, width=30, font=FONT)
    entry_quantidade.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(scrollable_frame, text="Tipo do Produto:", font=FONT).grid(row=2, column=0, padx=20, pady=10)
    entry_tipo_produto = tk.Entry(scrollable_frame, width=30, font=FONT)
    entry_tipo_produto.grid(row=2, column=1, padx=20, pady=10)

    tk.Label(scrollable_frame, text="ID da Instituição:", font=FONT).grid(row=3, column=0, padx=20, pady=10)
    entry_id_instituicao = tk.Entry(scrollable_frame, width=30, font=FONT)
    entry_id_instituicao.grid(row=3, column=1, padx=20, pady=10)

    def cadastrar():
        nome_produto = entry_nome_produto.get()
        quantidade = entry_quantidade.get()
        tipo_produto = entry_tipo_produto.get()
        id_instituicao = entry_id_instituicao.get()

        if not cadastrar_produto_estoque(nome_produto, quantidade, tipo_produto, id_instituicao):
            messagebox.showwarning("Erro", "Erro ao cadastrar produto no estoque. Por favor, verifique os dados inseridos.")
    
    tk.Button(scrollable_frame, text="Cadastrar Produto", font=FONT, command=cadastrar).grid(row=4, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_estoque(root)
    root.mainloop()
