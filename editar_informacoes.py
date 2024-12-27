import tkinter as tk
from tkinter import ttk
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def atualizar_informacoes(id_usuario, nome, endereco, telefone, email, observacao):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    UPDATE usuarios 
                    SET nome = :1, endereco = :2, telefone = :3, email = :4, observacao = :5
                    WHERE id_usuario = :6
                """
                cursor.execute(query, [nome, endereco, telefone, email, observacao, id_usuario])
                connection.commit()
                return True
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao atualizar informações: {e}")
        return False

def pagina_editar_informacoes(parent, id_usuario, nome, endereco, telefone, email, observacao):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="ID do Usuário:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_id_usuario = tk.Entry(frame, width=30, font=FONT)
    entry_id_usuario.grid(row=0, column=1, padx=20, pady=10)
    entry_id_usuario.insert(0, id_usuario)
    entry_id_usuario.config(state='disabled')

    tk.Label(frame, text="Nome:", font=FONT).grid(row=1, column=0, padx=20, pady=10)
    entry_nome = tk.Entry(frame, width=30, font=FONT)
    entry_nome.grid(row=1, column=1, padx=20, pady=10)
    entry_nome.insert(0, nome)

    tk.Label(frame, text="Endereço:", font=FONT).grid(row=2, column=0, padx=20, pady=10)
    entry_endereco = tk.Entry(frame, width=30, font=FONT)
    entry_endereco.grid(row=2, column=1, padx=20, pady=10)
    entry_endereco.insert(0, endereco)

    tk.Label(frame, text="Telefone:", font=FONT).grid(row=3, column=0, padx=20, pady=10)
    entry_telefone = tk.Entry(frame, width=30, font=FONT)
    entry_telefone.grid(row=3, column=1, padx=20, pady=10)
    entry_telefone.insert(0, telefone)

    tk.Label(frame, text="Email:", font=FONT).grid(row=4, column=0, padx=20, pady=10)
    entry_email = tk.Entry(frame, width=30, font=FONT)
    entry_email.grid(row=4, column=1, padx=20, pady=10)
    entry_email.insert(0, email)

    tk.Label(frame, text="Observação:", font=FONT).grid(row=5, column=0, padx=20, pady=10)
    entry_observacao = tk.Text(frame, width=30, height=5, font=FONT)
    entry_observacao.grid(row=5, column=1, padx=20, pady=10)
    entry_observacao.insert("1.0", observacao)

    def atualizar():
        novo_nome = entry_nome.get()
        novo_endereco = entry_endereco.get()
        novo_telefone = entry_telefone.get()
        novo_email = entry_email.get()
        nova_observacao = entry_observacao.get("1.0", "end-1c")

        if not atualizar_informacoes(id_usuario, novo_nome, novo_endereco, novo_telefone, novo_email, nova_observacao):
            print("Erro ao atualizar informações.")

    tk.Button(frame, text="Atualizar Informações", font=FONT, command=atualizar).grid(row=6, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_editar_informacoes(root, 1, "Nome Exemplo", "Endereço Exemplo", "Telefone Exemplo", "Email Exemplo", "Observação Exemplo")
    root.mainloop()
