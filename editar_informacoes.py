import tkinter as tk
from tkinter import ttk, messagebox
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
                messagebox.showinfo("Sucesso", "Informações atualizadas com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao atualizar informações: {e}")
        return False

def pagina_editar_informacoes(parent, id_usuario, nome, endereco, telefone, email, observacao):
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

    ttk.Label(scrollable_frame, text="ID do Usuário:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")
    entry_id_usuario = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_id_usuario.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    entry_id_usuario.insert(0, id_usuario)
    entry_id_usuario.config(state='disabled')

    ttk.Label(scrollable_frame, text="Nome:", font=FONT).grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_nome = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_nome.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    entry_nome.insert(0, nome)

    ttk.Label(scrollable_frame, text="Endereço:", font=FONT).grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_endereco = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_endereco.grid(row=2, column=1, padx=20, pady=10, sticky="w")
    entry_endereco.insert(0, endereco)

    ttk.Label(scrollable_frame, text="Telefone:", font=FONT).grid(row=3, column=0, padx=20, pady=10, sticky="e")
    entry_telefone = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_telefone.grid(row=3, column=1, padx=20, pady=10, sticky="w")
    entry_telefone.insert(0, telefone)

    ttk.Label(scrollable_frame, text="Email:", font=FONT).grid(row=4, column=0, padx=20, pady=10, sticky="e")
    entry_email = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_email.grid(row=4, column=1, padx=20, pady=10, sticky="w")
    entry_email.insert(0, email)

    ttk.Label(scrollable_frame, text="Observação:", font=FONT).grid(row=5, column=0, padx=20, pady=10, sticky="e")
    entry_observacao = tk.Text(scrollable_frame, width=30, height=5, font=FONT)
    entry_observacao.grid(row=5, column=1, padx=20, pady=10, sticky="w")
    entry_observacao.insert("1.0", observacao)

    def atualizar():
        novo_nome = entry_nome.get()
        novo_endereco = entry_endereco.get()
        novo_telefone = entry_telefone.get()
        novo_email = entry_email.get()
        nova_observacao = entry_observacao.get("1.0", "end-1c")

        if not atualizar_informacoes(id_usuario, novo_nome, novo_endereco, novo_telefone, novo_email, nova_observacao):
            messagebox.showerror("Erro", "Erro ao atualizar informações.")

    ttk.Button(scrollable_frame, text="Atualizar Informações", command=atualizar).grid(row=6, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_editar_informacoes(root, 1, "Nome Exemplo", "Endereço Exemplo", "Telefone Exemplo", "Email Exemplo", "Observação Exemplo")
    root.mainloop()
