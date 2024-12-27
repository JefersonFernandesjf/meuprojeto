import tkinter as tk
from tkinter import ttk, messagebox
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def carregar_instituicoes():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_instituicao, nome FROM instituicao")
                return cursor.fetchall()
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao carregar instituições: {e}")
        return []

def cadastrar_estoque(id_instituicao, tipo_produto, produto, quantidade):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO estoque (id_instituicao, tipo_produto, produto, quantidade, data_registro)
                    VALUES (:1, :2, :3, :4, SYSDATE)
                """
                cursor.execute(query, [id_instituicao, tipo_produto, produto, quantidade])
                connection.commit()
                messagebox.showinfo("Sucesso", "Produto cadastrado no estoque com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar produto no estoque: {e}")
        return False

def pagina_estoque(parent):
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

    ttk.Label(scrollable_frame, text="Selecione a Instituição:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")

    instituicoes = carregar_instituicoes()
    instituicoes_nomes = [f"{id_inst}: {nome}" for id_inst, nome in instituicoes]
    selected_instituicao = tk.StringVar(value=instituicoes_nomes[0] if instituicoes_nomes else "")

    instituicao_menu = ttk.Combobox(scrollable_frame, textvariable=selected_instituicao, values=instituicoes_nomes, state="readonly", font=FONT)
    instituicao_menu.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Tipo de Produto:", font=FONT).grid(row=1, column=0, padx=20, pady=10, sticky="e")
    tipo_produto_options = ["Limpeza", "Alimentação", "Igiene", "Ferramentas"]
    selected_tipo_produto = tk.StringVar(value=tipo_produto_options[0])
    tipo_produto_menu = ttk.Combobox(scrollable_frame, textvariable=selected_tipo_produto, values=tipo_produto_options, state="readonly", font=FONT)
    tipo_produto_menu.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Produto:", font=FONT).grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_produto = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_produto.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(scrollable_frame, text="Quantidade:", font=FONT).grid(row=3, column=0, padx=20, pady=10, sticky="e")
    entry_quantidade = ttk.Entry(scrollable_frame, width=30, font=FONT)
    entry_quantidade.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    def cadastrar():
        instituicao_selecionada = selected_instituicao.get().split(":")[0]
        tipo_produto = selected_tipo_produto.get()
        produto = entry_produto.get()
        quantidade = entry_quantidade.get()

        if cadastrar_estoque(instituicao_selecionada, tipo_produto, produto, quantidade):
            entry_produto.delete(0, tk.END)
            entry_quantidade.delete(0, tk.END)

    ttk.Button(scrollable_frame, text="Cadastrar Produto no Estoque", command=cadastrar).grid(row=4, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina_estoque(root)
    root.mainloop()
