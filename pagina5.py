import tkinter as tk
from tkinter import messagebox
from db_config import conectar_bd
from editar_usuario import pagina_editar_usuario
import cx_Oracle

FONT = ("Arial", 14)

def buscar_usuario(nome):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = '''
                    SELECT 
                        u.id_usuario, u.nome, u.endereco, u.telefone, u.email, u.observacao,
                        p.nome_produto, p.quantidade, p.categoria, 
                        e.medicamento, e.horario_administracao, e.data_registro,
                        q.numero_quarto, q.estado_quarto
                    FROM usuarios u
                    LEFT JOIN produtos_fornecidos p ON u.id_usuario = p.id_usuario
                    LEFT JOIN enfermaria e ON u.id_usuario = e.id_usuario
                    LEFT JOIN quartos q ON u.id_usuario = q.id_usuario
                    WHERE u.nome = :nome
                '''
                cursor.execute(query, {"nome": nome})
                resultados = cursor.fetchall()

                if resultados:
                    informacoes = ""
                    for linha in resultados:
                        informacoes += f"ID: {linha[0]}\n"
                        informacoes += f"Nome: {linha[1]}\nEndereço: {linha[2]}\nTelefone: {linha[3]}\nEmail: {linha[4]}\n"
                        informacoes += f"Observação: {linha[5]}\n"
                        informacoes += f"Produto Fornecido: {linha[6]} - Quantidade: {linha[7]} - Categoria: {linha[8]}\n"
                        informacoes += f"Medicamento: {linha[9]} - Horário: {linha[10]} - Data: {linha[11]}\n"
                        informacoes += f"Número do Quarto: {linha[12]} - Estado do Quarto: {linha[13]}\n\n"
                    return informacoes, resultados[0]  # Retorna a informação e a linha completa
                else:
                    return "Usuário não encontrado.", None
    except cx_Oracle.DatabaseError as e:
        return f"Erro ao buscar dados: {e}", None

def excluir_usuario(id_usuario):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                # Excluir registros filhos
                cursor.execute("DELETE FROM produtos_fornecidos WHERE id_usuario = :1", [id_usuario])
                cursor.execute("DELETE FROM enfermaria WHERE id_usuario = :1", [id_usuario])
                cursor.execute("DELETE FROM quartos WHERE id_usuario = :1", [id_usuario])

                # Excluir registro pai
                cursor.execute("DELETE FROM usuarios WHERE id_usuario = :1", [id_usuario])
                
                connection.commit()
                messagebox.showinfo("Sucesso", "Usuário e registros relacionados excluídos com sucesso!")
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao excluir usuário e registros relacionados: {e}")
        return False
    return True

def abrir_pesquisa(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Nome do Usuário:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_nome = tk.Entry(frame, width=30, font=FONT)
    entry_nome.grid(row=0, column=1, padx=20, pady=10)

    def exibir_resultados():
        # Limpar widgets existentes (evitar duplicação)
        for widget in frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        nome = entry_nome.get()
        resultados, dados_usuario = buscar_usuario(nome)
        resultados_label = tk.Label(frame, text=resultados, font=FONT, justify="left")
        resultados_label.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        if dados_usuario:
            id_usuario, nome, endereco, telefone, email, observacao, *_ = dados_usuario
            tk.Button(frame, text="Editar Informações do Usuário", font=FONT, command=lambda: pagina_editar_usuario(id_usuario, nome, endereco, telefone, email, observacao)).grid(row=3, column=0, padx=20, pady=10)
            tk.Button(frame, text="Excluir Usuário", font=FONT, command=lambda: excluir_usuario(id_usuario)).grid(row=3, column=1, padx=20, pady=10)

    tk.Button(frame, text="Pesquisar", font=FONT, command=exibir_resultados).grid(row=1, column=0, columnspan=2, padx=20, pady=10)

def mostrar_ids(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="IDs de Usuários:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario, nome FROM usuarios")
                usuarios = cursor.fetchall()
                texto_usuarios = "\n".join([f"{id_usuario}: {nome}" for id_usuario, nome in usuarios])
                tk.Label(frame, text=texto_usuarios, font=FONT, justify="left").grid(row=1, column=0, padx=20, pady=10)
    except cx_Oracle.DatabaseError as e:
        tk.messagebox.showerror("Erro", f"Erro ao buscar IDs de usuários: {e}")

    tk.Label(frame, text="IDs de Instituições:", font=FONT).grid(row=0, column=1, padx=20, pady=10)
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_instituicao, nome FROM instituicao")
                instituicoes = cursor.fetchall()
                texto_instituicoes = "\n".join([f"{id_instituicao}: {nome}" for id_instituicao, nome in instituicoes])
                tk.Label(frame, text=texto_instituicoes, font=FONT, justify="left").grid(row=1, column=1, padx=20, pady=10)
    except cx_Oracle.DatabaseError as e:
        tk.messagebox.showerror("Erro", f"Erro ao buscar IDs de instituições: {e}")

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    abrir_pesquisa(root)
    root.mainloop()
