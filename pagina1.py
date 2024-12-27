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

    ttk.Label(scrollable_frame, text="Nome da Instituição:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")
    entry_nome = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_nome.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Endereço:", font=FONT).grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_endereco = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_endereco.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Telefone:", font=FONT).grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_telefone = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_telefone.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Email:", font=FONT).grid(row=3, column=0, padx=20, pady=10, sticky="e")
    entry_email = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_email.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    def cadastrar():
        nome = entry_nome.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        email = entry_email.get()

        if not cadastrar_instituicao(nome, endereco, telefone, email):
            messagebox.showwarning("Erro", "Erro ao cadastrar instituição. Por favor, verifique os dados inseridos.")
    
    ttk.Button(scrollable_frame, text="Cadastrar Instituição", command=cadastrar).grid(row=4, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina1(root)
    root.mainloop()
