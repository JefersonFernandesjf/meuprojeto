import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def cadastrar_instituicao(nome, endereco, telefone, email):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO instituicao (nome, endereco, telefone, email)
                    VALUES (:1, :2, :3, :4)
                """
                cursor.execute(query, [nome, endereco, telefone, email])
                connection.commit()
                messagebox.showinfo("Sucesso", "Instituição cadastrada com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar instituição: {e}")
        return False

def pagina1(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Nome da Instituição:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_nome = tk.Entry(frame, width=30, font=FONT)
    entry_nome.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(frame, text="Endereço:", font=FONT).grid(row=1, column=0, padx=20, pady=10)
    entry_endereco = tk.Entry(frame, width=30, font=FONT)
    entry_endereco.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(frame, text="Telefone:", font=FONT).grid(row=2, column=0, padx=20, pady=10)
    entry_telefone = tk.Entry(frame, width=30, font=FONT)
    entry_telefone.grid(row=2, column=1, padx=20, pady=10)

    tk.Label(frame, text="Email:", font=FONT).grid(row=3, column=0, padx=20, pady=10)
    entry_email = tk.Entry(frame, width=30, font=FONT)
    entry_email.grid(row=3, column=1, padx=20, pady=10)

    def cadastrar():
        nome = entry_nome.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        email = entry_email.get()

        if not cadastrar_instituicao(nome, endereco, telefone, email):
            messagebox.showwarning("Erro", "Erro ao cadastrar instituição. Por favor, verifique os dados inseridos.")
    
    tk.Button(frame, text="Cadastrar Instituição", font=FONT, command=cadastrar).grid(row=4, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina1(root)
    root.mainloop()
