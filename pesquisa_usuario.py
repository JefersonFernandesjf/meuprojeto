import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def buscar_informacoes_usuario(id_usuario):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = "SELECT * FROM usuarios WHERE id_usuario = :1"
                cursor.execute(query, [id_usuario])
                return cursor.fetchone()
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao buscar informações do usuário: {e}")
        return None

def pagina_pesquisa_usuario(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="ID do Usuário:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")
    entry_id_usuario = ttk.Entry(frame, width=30, font=FONT)
    entry_id_usuario.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    def pesquisar():
        id_usuario = entry_id_usuario.get()
        if not id_usuario:
            messagebox.showwarning("Aviso", "Por favor, insira o ID do usuário.")
            return

        info_usuario = buscar_informacoes_usuario(id_usuario)
        if info_usuario:
            info_text = f"""
            ID do Usuário: {info_usuario[0]}
            Nome: {info_usuario[1]}
            Endereço: {info_usuario[2]}
            Telefone: {info_usuario[3]}
            Email: {info_usuario[4]}
            Observação: {info_usuario[5]}
            ID da Instituição: {info_usuario[6]}
            """
            messagebox.showinfo("Informações do Usuário", info_text)
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    ttk.Button(frame, text="Pesquisar", command=pesquisar).grid(row=1, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_pesquisa_usuario(root)
    root.mainloop()
