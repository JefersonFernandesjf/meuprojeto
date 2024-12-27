import tkinter as tk
from tkinter import messagebox
from db_config import DB_USER, DB_PASSWORD, DB_DSN
import cx_Oracle

FONT = ("Arial", 14)

def editar_usuario(id_usuario, nome, endereco, telefone, email, observacao):
    try:
        with cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN) as connection:
            with connection.cursor() as cursor:
                query = """
                    UPDATE usuarios
                    SET nome = :1, endereco = :2, telefone = :3, email = :4, observacao = :5
                    WHERE id_usuario = :6
                """
                cursor.execute(query, [nome, endereco, telefone, email, observacao, id_usuario])
                connection.commit()
                messagebox.showinfo("Sucesso", "Informações do usuário atualizadas com sucesso!")
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao atualizar informações do usuário: {e}")
        return False
    return True

def pagina_editar_usuario(id_usuario, nome_atual, endereco_atual, telefone_atual, email_atual, observacao_atual):
    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Informações do Usuário")

    tk.Label(janela_editar, text="Nome do Usuário:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_nome_usuario = tk.Entry(janela_editar, width=30, font=FONT)
    entry_nome_usuario.grid(row=0, column=1, padx=20, pady=10)
    entry_nome_usuario.insert(0, nome_atual)

    tk.Label(janela_editar, text="Endereço:", font=FONT).grid(row=1, column=0, padx=20, pady=10)
    entry_endereco_usuario = tk.Entry(janela_editar, width=30, font=FONT)
    entry_endereco_usuario.grid(row=1, column=1, padx=20, pady=10)
    entry_endereco_usuario.insert(0, endereco_atual)

    tk.Label(janela_editar, text="Telefone:", font=FONT).grid(row=2, column=0, padx=20, pady=10)
    entry_telefone_usuario = tk.Entry(janela_editar, width=30, font=FONT)
    entry_telefone_usuario.grid(row=2, column=1, padx=20, pady=10)
    entry_telefone_usuario.insert(0, telefone_atual)

    tk.Label(janela_editar, text="Email:", font=FONT).grid(row=3, column=0, padx=20, pady=10)
    entry_email_usuario = tk.Entry(janela_editar, width=30, font=FONT)
    entry_email_usuario.grid(row=3, column=1, padx=20, pady=10)
    entry_email_usuario.insert(0, email_atual)

    tk.Label(janela_editar, text="Observação (até 200 caracteres):", font=FONT).grid(row=4, column=0, padx=20, pady=10)
    entry_observacao = tk.Text(janela_editar, width=30, height=5, font=FONT)
    entry_observacao.grid(row=4, column=1, padx=20, pady=10)
    entry_observacao.insert("1.0", observacao_atual)

    def salvar_alteracoes():
        nome_usuario = entry_nome_usuario.get()
        endereco_usuario = entry_endereco_usuario.get()
        telefone_usuario = entry_telefone_usuario.get()
        email_usuario = entry_email_usuario.get()
        observacao = entry_observacao.get("1.0", "end-1c")

        if len(observacao) > 200:
            messagebox.showwarning("Aviso", "Observação deve ter no máximo 200 caracteres.")
            return

        if not editar_usuario(id_usuario, nome_usuario, endereco_usuario, telefone_usuario, email_usuario, observacao):
            messagebox.showwarning("Erro", "Erro ao atualizar informações do usuário. Por favor, verifique os dados inseridos.")

    tk.Button(janela_editar, text="Salvar Alterações", font=FONT, command=salvar_alteracoes).grid(row=5, column=0, columnspan=2, padx=20, pady=10)
