import tkinter as tk
from tkinter import ttk
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def cadastrar_usuario(nome, endereco, telefone, email, observacao, id_instituicao):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO usuarios (nome, endereco, telefone, email, observacao, id_instituicao)
                    VALUES (:1, :2, :3, :4, :5, :6)
                """
                cursor.execute(query, [nome, endereco, telefone, email, observacao, id_instituicao])
                connection.commit()
                return True
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False

def cadastrar_medicamento_particular(id_usuario, nome_medicamento, quantidade):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO medicamentos_particulares (id_usuario, nome_medicamento, quantidade)
                    VALUES (:1, :2, :3)
                """
                cursor.execute(query, [id_usuario, nome_medicamento, quantidade])
                connection.commit()
                print("Medicamento particular cadastrado com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao cadastrar medicamento particular: {e}")
        return False

def cadastrar_medicamento_enfermaria(id_usuario, nome_medicamento, quantidade, id_enfermaria):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO medicamentos_enfermaria (id_usuario, nome_medicamento, quantidade, id_enfermaria)
                    VALUES (:1, :2, :3, :4)
                """
                cursor.execute(query, [id_usuario, nome_medicamento, quantidade, id_enfermaria])

                # Atualizar o estoque da enfermaria
                query_estoque = """
                    UPDATE estoque
                    SET quantidade = quantidade - :1
                    WHERE id_instituicao = :2 AND nome_produto = :3
                """
                cursor.execute(query_estoque, [quantidade, id_enfermaria, nome_medicamento])

                connection.commit()
                print("Medicamento da enfermaria cadastrado e estoque atualizado com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao cadastrar medicamento da enfermaria: {e}")
        return False

def buscar_instituicoes():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = "SELECT id_instituicao, nome FROM instituicao"
                cursor.execute(query)
                return cursor.fetchall()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao buscar instituições: {e}")
        return []

def buscar_id_usuario(nome):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = "SELECT id_usuario FROM usuarios WHERE nome = :1"
                cursor.execute(query, [nome])
                resultado = cursor.fetchone()
                return resultado[0] if resultado else None
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao buscar ID do usuário: {e}")
        return None

def pagina2(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Nome do Usuário:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_nome_usuario = tk.Entry(frame, width=30, font=FONT)
    entry_nome_usuario.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(frame, text="Endereço:", font=FONT).grid(row=1, column=0, padx=20, pady=10)
    entry_endereco_usuario = tk.Entry(frame, width=30, font=FONT)
    entry_endereco_usuario.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(frame, text="Telefone:", font=FONT).grid(row=2, column=0, padx=20, pady=10)
    entry_telefone_usuario = tk.Entry(frame, width=30, font=FONT)
    entry_telefone_usuario.grid(row=2, column=1, padx=20, pady=10)

    tk.Label(frame, text="Email:", font=FONT).grid(row=3, column=0, padx=20, pady=10)
    entry_email_usuario = tk.Entry(frame, width=30, font=FONT)
    entry_email_usuario.grid(row=3, column=1, padx=20, pady=10)

    tk.Label(frame, text="Observação (até 200 caracteres):", font=FONT).grid(row=4, column=0, padx=20, pady=10)
    entry_observacao = tk.Text(frame, width=30, height=5, font=FONT)
    entry_observacao.grid(row=4, column=1, padx=20, pady=10)

    tk.Label(frame, text="Instituição:", font=FONT).grid(row=5, column=0, padx=20, pady=10)
    combo_instituicao = ttk.Combobox(frame, width=28, font=FONT)
    combo_instituicao.grid(row=5, column=1, padx=20, pady=10)

    instituicoes = buscar_instituicoes()
    combo_instituicao['values'] = [f"{id} - {nome}" for id, nome in instituicoes]

    frame_medicamentos = tk.Frame(frame)
    frame_medicamentos.grid(row=6, column=0, columnspan=2, pady=10)

    tk.Label(frame_medicamentos, text="Nome do Medicamento", font=FONT).grid(row=0, column=0, padx=20, pady=5)
    tk.Label(frame_medicamentos, text="Quantidade", font=FONT).grid(row=0, column=1, padx=20, pady=5)
    tk.Label(frame_medicamentos, text="Enfermaria (ID)", font=FONT).grid(row=0, column=2, padx=20, pady=5)

    medicamentos = []

    def adicionar_medicamento():
        linha = len(medicamentos)
        entry_nome_medicamento = tk.Entry(frame_medicamentos, width=30, font=FONT)
        entry_nome_medicamento.grid(row=linha + 1, column=0, padx=20, pady=5)
        entry_quantidade = tk.Entry(frame_medicamentos, width=30, font=FONT)
        entry_quantidade.grid(row=linha + 1, column=1, padx=20, pady=5)
        entry_id_enfermaria = tk.Entry(frame_medicamentos, width=30, font=FONT)
        entry_id_enfermaria.grid(row=linha + 1, column=2, padx=20, pady=5)
        medicamentos.append({'nome': entry_nome_medicamento, 'quantidade': entry_quantidade, 'id_enfermaria': entry_id_enfermaria})

    tk.Button(frame, text="Adicionar Medicamento", font=FONT, command=adicionar_medicamento).grid(row=7, column=0, columnspan=2, pady=10)

    def cadastrar():
        nome_usuario = entry_nome_usuario.get()
        endereco_usuario = entry_endereco_usuario.get()
        telefone_usuario = entry_telefone_usuario.get()
        email_usuario = entry_email_usuario.get()
        observacao = entry_observacao.get("1.0", "end-1c")
        instituicao_selecionada = combo_instituicao.get()

        if instituicao_selecionada:
            id_instituicao = int(instituicao_selecionada.split(" - ")[0])
        else:
            print("Aviso: Por favor, selecione uma instituição.")
            return

        if len(observacao) > 200:
            print("Aviso: Observação deve ter no máximo 200 caracteres.")
            return

        if not cadastrar_usuario(nome_usuario, endereco_usuario, telefone_usuario, email_usuario, observacao, id_instituicao):
            return

        id_usuario = buscar_id_usuario(nome_usuario)
        medicamentos_particulares = [medicamento for medicamento in medicamentos if not medicamento['id_enfermaria'].get()]
        medicamentos_enfermaria = [medicamento for medicamento in medicamentos if medicamento['id_enfermaria'].get()]

        for medicamento in medicamentos_particulares:
            cadastrar_medicamento_particular(id_usuario, medicamento['nome'].get(), medicamento['quantidade'].get())

        for medicamento in medicamentos_enfermaria:
            cadastrar_medicamento_enfermaria(id_usuario, medicamento['nome'].get(), medicamento['quantidade'].get(), medicamento['id_enfermaria'].get())

    tk.Button(frame, text="Cadastrar Usuário", font=FONT, command=cadastrar).grid(row=8, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina2(root)
    root.mainloop()
