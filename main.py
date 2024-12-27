import logging
import tkinter as tk
from tkinter import ttk

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', filename='app.log')
logger = logging.getLogger()

# Importar as páginas
from pagina1 import pagina1
from pagina_estoque import pagina_estoque
from pagina2 import pagina2
from pagina3 import pagina3
from pagina4 import pagina4
from pagina5 import abrir_pesquisa, mostrar_ids
from pagina_informacoes_enfermaria import pagina_informacoes_enfermaria
from editar_informacoes import pagina_editar_informacoes
from settings import mudar_cor_interface, editar_configuracao, atualizar_programa

def main():
    logger.info('Iniciando o programa...')
    
    root = tk.Tk()
    root.title("Sistema de Gerenciamento de Instituição")
    root.state('zoomed')  # Abre a janela em tela cheia

    menubar = tk.Menu(root)
    config_menu = tk.Menu(menubar, tearoff=0)
    config_menu.add_command(label="Mudar Cor da Interface", command=lambda: mudar_cor_interface(root))
    config_menu.add_command(label="Editar Configurações do Banco de Dados", command=editar_configuracao)
    config_menu.add_command(label="Atualizar Programa", command=atualizar_programa)
    menubar.add_cascade(label="Configurações", menu=config_menu)
    root.config(menu=menubar)

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=10)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(side="top", fill="x")

    canvas = tk.Canvas(frame_buttons)
    canvas.pack(side="left", fill="x", expand=True)

    scrollbar = ttk.Scrollbar(frame_buttons, orient="horizontal", command=canvas.xview)
    scrollbar.pack(side="bottom", fill="x")

    button_frame = tk.Frame(canvas)
    button_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=button_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    frame_content = tk.Frame(root)
    frame_content.pack(fill="both", expand=True)

    def show_page(page):
        for widget in frame_content.winfo_children():
            widget.destroy()
        page(frame_content)

    buttons = [
        ("Cadastro de Instituição", pagina1),
        ("Estoque da Instituição", pagina_estoque),
        ("Cadastro de Usuário", pagina2),
        ("Produtos na Enfermaria", pagina3),
        ("Cadastro de Quartos", pagina4),
        ("Pesquisa de Usuários", abrir_pesquisa),
        ("IDs de Usuários e Instituições", mostrar_ids),
        ("Informações da Enfermaria", pagina_informacoes_enfermaria),
        ("Editar Informações", pagina_editar_informacoes)
    ]

    for (text, page) in buttons:
        ttk.Button(button_frame, text=text, command=lambda p=page: show_page(p), style="TButton").pack(side="left", padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
