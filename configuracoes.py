import tkinter as tk
from tkinter import messagebox, colorchooser
from db_config import DB_USER, DB_PASSWORD, DB_DSN

def salvar_configuracoes(usuario, senha, dsn, cor):
    # Salva as configurações em um arquivo de configuração ou base de dados
    with open("config.txt", "w") as file:
        file.write(f"{usuario}\n{senha}\n{dsn}\n{cor}")

def carregar_configuracoes():
    # Carrega as configurações do arquivo de configuração ou base de dados
    try:
        with open("config.txt", "r") as file:
            config = file.read().splitlines()
            return config
    except FileNotFoundError:
        return [DB_USER, DB_PASSWORD, DB_DSN, "#f0f0f0"]

def abrir_configuracoes():
    janela = tk.Toplevel()
    janela.title("Configurações")

    config = carregar_configuracoes()
    usuario, senha, dsn, cor = config

    tk.Label(janela, text="Usuário:").grid(row=0, column=0, padx=10, pady=5)
    entry_usuario = tk.Entry(janela, width=30)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)
    entry_usuario.insert(0, usuario)

    tk.Label(janela, text="Senha:").grid(row=1, column=0, padx=10, pady=5)
    entry_senha = tk.Entry(janela, show="*", width=30)
    entry_senha.grid(row=1, column=1, padx=10, pady=5)
    entry_senha.insert(0, senha)

    tk.Label(janela, text="DSN:").grid(row=2, column=0, padx=10, pady=5)
    entry_dsn = tk.Entry(janela, width=30)
    entry_dsn.grid(row=2, column=1, padx=10, pady=5)
    entry_dsn.insert(0, dsn)

    tk.Label(janela, text="Cor da Interface:").grid(row=3, column=0, padx=10, pady=5)
    canvas_cor = tk.Canvas(janela, bg=cor, width=50, height=20)
    canvas_cor.grid(row=3, column=1, padx=10, pady=5)

    def escolher_cor():
        cor = colorchooser.askcolor()[1]
        if cor:
            canvas_cor.config(bg=cor)

    tk.Button(janela, text="Escolher Cor", command=escolher_cor).grid(row=4, column=0, columnspan=2, pady=10)

    def salvar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        dsn = entry_dsn.get()
        cor = canvas_cor.cget("bg")
        salvar_configuracoes(usuario, senha, dsn, cor)
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).grid(row=5, column=0, columnspan=2, pady=10)
