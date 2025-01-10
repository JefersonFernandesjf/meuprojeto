import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def atualizar_informacoes_usuario(id_usuario, nome, endereco, telefone, email, observacao):
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
                messagebox.showinfo("Sucesso", "Informações do usuário atualizadas com sucesso!")
                print("Informações do usuário atualizadas com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao atualizar informações do usuário: {e}")
        print(f"Erro ao atualizar informações do usuário: {e}")
        return False

def atualizar_informacoes_instituicao(id_instituicao, nome_instituicao, endereco_instituicao, telefone_instituicao, email_instituicao):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    UPDATE instituicao 
                    SET nome = :1, endereco = :2, telefone = :3, email = :4
                    WHERE id_instituicao = :5
                """
                cursor.execute(query, [nome_instituicao, endereco_instituicao, telefone_instituicao, email_instituicao, id_instituicao])
                connection.commit()
                messagebox.showinfo("Sucesso", "Informações da instituição atualizadas com sucesso!")
                print("Informações da instituição atualizadas com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao atualizar informações da instituição: {e}")
        print(f"Erro ao atualizar informações da instituição: {e}")
        return False

def atualizar_informacoes_enfermaria(id_enfermaria, nome_enfermaria, id_instituicao):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    UPDATE enfermaria 
                    SET nome = :1, id_instituicao = :2
                    WHERE id_enfermaria = :3
                """
                cursor.execute(query, [nome_enfermaria, id_instituicao, id_enfermaria])
                connection.commit()
                messagebox.showinfo("Sucesso", "Informações da enfermaria atualizadas com sucesso!")
                print("Informações da enfermaria atualizadas com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao atualizar informações da enfermaria: {e}")
        print(f"Erro ao atualizar informações da enfermaria: {e}")
        return False

def carregar_informacoes_usuario(id_usuario):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = "SELECT nome, endereco, telefone, email, observacao, id_instituicao FROM usuarios WHERE id_usuario = :1"
                cursor.execute(query, [id_usuario])
                usuario_info = cursor.fetchone()
                print(f"Resultado da consulta para usuário com ID {id_usuario}: {usuario_info}")
                return usuario_info
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao carregar informações do usuário: {e}")
        print(f"Erro ao carregar informações do usuário: {e}")
        return None

def carregar_informacoes_instituicao(id_instituicao):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = "SELECT nome, endereco, telefone, email FROM instituicao WHERE id_instituicao = :1"
                cursor.execute(query, [id_instituicao])
                instituicao_info = cursor.fetchone()
                print(f"Resultado da consulta para instituição com ID {id_instituicao}: {instituicao_info}")
                return instituicao_info
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao carregar informações da instituição: {e}")
        print(f"Erro ao carregar informações da instituição: {e}")
        return None

def carregar_informacoes_enfermaria(id_enfermaria):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = "SELECT nome, id_instituicao FROM enfermaria WHERE id_enfermaria = :1"
                cursor.execute(query, [id_enfermaria])
                enfermaria_info = cursor.fetchone()
                print(f"Resultado da consulta para enfermaria com ID {id_enfermaria}: {enfermaria_info}")
                return enfermaria_info
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao carregar informações da enfermaria: {e}")
        print(f"Erro ao carregar informações da enfermaria: {e}")
        return None

def pagina_editar_informacoes(parent, id_usuario, id_instituicao, id_enfermaria):
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

    # Carregar informações do usuário
    usuario_info = carregar_informacoes_usuario(id_usuario)
    if usuario_info:
        nome, endereco, telefone, email, observacao, id_instituicao_usuario = usuario_info
        instituicao_info_usuario = carregar_informacoes_instituicao(id_instituicao_usuario)
        if instituicao_info_usuario:
            nome_instituicao_usuario, endereco_instituicao_usuario, telefone_instituicao_usuario, email_instituicao_usuario = instituicao_info_usuario
        else:
            nome_instituicao_usuario = endereco_instituicao_usuario = telefone_instituicao_usuario = email_instituicao_usuario = ""

        ttk.Label(scrollable_frame, text="ID do Usuário:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")
        entry_id_usuario = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_id_usuario.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        entry_id_usuario.insert(0, id_usuario)
        entry_id_usuario.config(state='disabled')

        ttk.Label(scrollable_frame, text="Nome do Usuário:", font=FONT).grid(row=1, column=0, padx=20, pady=10, sticky="e")
        entry_nome = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_nome.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        entry_nome.insert(0, nome)

        ttk.Label(scrollable_frame, text="Endereço do Usuário:", font=FONT).grid(row=2, column=0, padx=20, pady=10, sticky="e")
        entry_endereco = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_endereco.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        entry_endereco.insert(0, endereco)

        ttk.Label(scrollable_frame, text="Telefone do Usuário:", font=FONT).grid(row=3, column=0, padx=20, pady=10, sticky="e")
        entry_telefone = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_telefone.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        entry_telefone.insert(0, telefone)

        ttk.Label(scrollable_frame, text="Email do Usuário:", font=FONT).grid(row=4, column=0, padx=20, pady=10, sticky="e")
        entry_email = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_email.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        entry_email.insert(0, email)

        ttk.Label(scrollable_frame, text="Observação do Usuário:", font=FONT).grid(row=5, column=0, padx=20, pady=10, sticky="e")
        entry_observacao = tk.Text(scrollable_frame, width=30, height=5, font=FONT)
        entry_observacao.grid(row=5, column=1, padx=20, pady=10, sticky="w")
        entry_observacao.insert("1.0", observacao)

    # Carregar informações da instituição
    instituicao_info = carregar_informacoes_instituicao(id_instituicao)
    if instituicao_info:
        nome_instituicao, endereco_instituicao, telefone_instituicao, email_instituicao = instituicao_info
        ttk.Label(scrollable_frame, text="ID da Instituição:", font=FONT).grid(row=6, column=0, padx=20, pady=10, sticky="e")
        entry_id_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_id_instituicao.grid(row=6, column=1, padx=20, pady=10, sticky="w")
        entry_id_instituicao.insert(0, id_instituicao)
        entry_id_instituicao.config(state='disabled')

        ttk.Label(scrollable_frame, text="Nome da Instituição:", font=FONT).grid(row=7, column=0, padx=20, pady=10, sticky="e")
        entry_nome_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_nome_instituicao.grid(row=7, column=1, padx=20, pady=10, sticky="w")
        entry_nome_instituicao.insert(0, nome_instituicao)

        ttk.Label(scrollable_frame, text="Endereço da Instituição:", font=FONT).grid(row=8, column=0, padx=20, pady=10, sticky="e")
        entry_endereco_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_endereco_instituicao.grid(row=8, column=1, padx=20, pady=10, sticky="w")
        entry_endereco_instituicao.insert(0, endereco_instituicao)

        ttk.Label(scrollable_frame, text="Telefone da Instituição:", font=FONT).grid(row=9, column=0, padx=20, pady=10, sticky="e")
        entry_telefone_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_telefone_instituicao.grid(row=9, column=1, padx=20, pady=10, sticky="w")
        entry_telefone_instituicao.insert(0, telefone_instituicao)

        ttk.Label(scrollable_frame, text="Email da Instituição:", font=FONT).grid(row=10, column=0, padx=20, pady=10, sticky="e")
        entry_email_instituicao = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_email_instituicao.grid(row=10, column=1, padx=20, pady=10, sticky="w")
        entry_email_instituicao.insert(0, email_instituicao)

    # Carregar informações da enfermaria
    enfermaria_info = carregar_informacoes_enfermaria(id_enfermaria)
    if enfermaria_info:
        nome_enfermaria, id_instituicao_enfermaria = enfermaria_info
        ttk.Label(scrollable_frame, text="ID da Enfermaria:", font=FONT).grid(row=11, column=0, padx=20, pady=10, sticky="e")
        entry_id_enfermaria = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_id_enfermaria.grid(row=11, column=1, padx=20, pady=10, sticky="w")
        entry_id_enfermaria.insert(0, id_enfermaria)
        entry_id_enfermaria.config(state='disabled')

        ttk.Label(scrollable_frame, text="Nome da Enfermaria:", font=FONT).grid(row=12, column=0, padx=20, pady=10, sticky="e")
        entry_nome_enfermaria = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_nome_enfermaria.grid(row=12, column=1, padx=20, pady=10, sticky="w")
        entry_nome_enfermaria.insert(0, nome_enfermaria)

        ttk.Label(scrollable_frame, text="ID da Instituição Associada:", font=FONT).grid(row=13, column=0, padx=20, pady=10, sticky="e")
        entry_id_instituicao_enfermaria = ttk.Entry(scrollable_frame, width=30, font=FONT)
        entry_id_instituicao_enfermaria.grid(row=13, column=1, padx=20, pady=10, sticky="w")
        entry_id_instituicao_enfermaria.insert(0, id_instituicao_enfermaria)
        entry_id_instituicao_enfermaria.config(state='disabled')

    # Função para atualizar informações
    def atualizar():
        # Atualizar informações do usuário
        novo_nome = entry_nome.get()
        novo_endereco = entry_endereco.get()
        novo_telefone = entry_telefone.get()
        novo_email = entry_email.get()
        nova_observacao = entry_observacao.get("1.0", "end-1c")

        # Atualizar informações da instituição
        nome_nova_instituicao = entry_nome_instituicao.get()
        endereco_nova_instituicao = entry_endereco_instituicao.get()
        telefone_nova_instituicao = entry_telefone_instituicao.get()
        email_novo_instituicao = entry_email_instituicao.get()

        # Atualizar informações da enfermaria
        nome_nova_enfermaria = entry_nome_enfermaria.get()
        id_instituicao_associada = id_instituicao_enfermaria

        if not atualizar_informacoes_usuario(id_usuario, novo_nome, novo_endereco, novo_telefone, novo_email, nova_observacao):
            return
        if not atualizar_informacoes_instituicao(id_instituicao, nome_nova_instituicao, endereco_nova_instituicao, telefone_nova_instituicao, email_novo_instituicao):
            return
        if not atualizar_informacoes_enfermaria(id_enfermaria, nome_nova_enfermaria, id_instituicao_associada):
            return

    ttk.Button(scrollable_frame, text="Atualizar Informações", command=atualizar).grid(row=14, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_editar_informacoes(root, 1, 1, 1)  # Substitua "1" pelos IDs reais
    root.deiconify()  # Mostrar a janela principal
    root.mainloop()
