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
    root.geometry("1024x768")  # Tamanho inicial da janela

    # Aplicar tema
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", font=("Arial", 12), padding=6)
    style.configure("TLabel", font=("Arial", 14))
    style.configure("TEntry", font=("Arial", 14))

    menubar = tk.Menu(root)
    config_menu = tk.Menu(menubar, tearoff=0)
    config_menu.add_command(label="Mudar Cor da Interface", command=lambda: mudar_cor_interface(root))
    config_menu.add_command(label="Editar Configurações do Banco de Dados", command=editar_configuracao)
    config_menu.add_command(label="Atualizar Programa", command=atualizar_programa)
    menubar.add_cascade(label="Configurações", menu=config_menu)
    root.config(menu=menubar)

    # Frame para os botões de navegação
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(side="left", fill="y", padx=10, pady=10)

    # Barra de rolagem vertical
    canvas = tk.Canvas(frame_buttons)
    scrollbar = ttk.Scrollbar(frame_buttons, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame para o conteúdo das páginas
    frame_content = tk.Frame(root)
    frame_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

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

    for text, page in buttons:
        ttk.Button(scrollable_frame, text=text, command=lambda p=page: show_page(p), style="TButton").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
