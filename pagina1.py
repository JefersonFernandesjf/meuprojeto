import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def cadastrar_instituicao(nome, endereco, telefone, email, enfermaria):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                # Inserir instituição usando a sequência
                query_instituicao = """
                    INSERT INTO instituicao (id_instituicao, nome, endereco, telefone, email)
                    VALUES (instituicao_seq.NEXTVAL, :1, :2, :3, :4)
                """
                cursor.execute(query_instituicao, [nome, endereco, telefone, email])

                # Inserir enfermaria associada usando a sequência
                query_enfermaria = """
                    INSERT INTO enfermaria (id_enfermaria, nome, id_instituicao)
                    VALUES (enfermaria_seq.NEXTVAL, :1, instituicao_seq.CURRVAL)
                """
                cursor.execute(query_enfermaria, [enfermaria])

                connection.commit()
                messagebox.showinfo("Sucesso", "Instituição e Enfermaria cadastradas com sucesso!")
                return True
    except cx_Oracle.IntegrityError as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar instituição e enfermaria: {e}")
        return False
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
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

    # Formulário de Cadastro de Instituição
    ttk.Label(scrollable_frame, text="Nome da Instituição:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")
    entry_nome_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_nome_instituicao.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Endereço:", font=FONT).grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_endereco_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_endereco_instituicao.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Telefone:", font=FONT).grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_telefone_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_telefone_instituicao.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Email:", font=FONT).grid(row=3, column=0, padx=20, pady=10, sticky="e")
    entry_email_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_email_instituicao.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    # Formulário de Cadastro de Enfermaria (apenas o nome)
    ttk.Label(scrollable_frame, text="Nome da Enfermaria:", font=FONT).grid(row=4, column=0, padx=20, pady=10, sticky="e")
    entry_nome_enfermaria = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_nome_enfermaria.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    def cadastrar():
        nome = entry_nome_instituicao.get()
        endereco = entry_endereco_instituicao.get()
        telefone = entry_telefone_instituicao.get()
        email = entry_email_instituicao.get()
        enfermaria = entry_nome_enfermaria.get()

        if not cadastrar_instituicao(nome, endereco, telefone, email, enfermaria):
            messagebox.showwarning("Erro", "Erro ao cadastrar instituição e enfermaria. Por favor, verifique os dados inseridos.")

    ttk.Button(scrollable_frame, text="Cadastrar Instituição e Enfermaria", command=cadastrar).grid(row=5, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina1(root)
    root.deiconify()  # Mostrar a janela principal
    root.mainloop()
