import tkinter as tk
from tkinter import ttk

from pagina1 import pagina1
from pagina_estoque import pagina_estoque
from pagina2 import pagina2
from pagina3 import pagina3
from pagina4 import pagina4
from pagina5 import mostrar_ids
from pagina_informacoes_enfermaria import pagina_informacoes_enfermaria
from editar_informacoes import pagina_editar_informacoes
from settings import mudar_cor_interface, editar_configuracao, atualizar_programa
from pesquisa_usuario import pagina_pesquisa_usuario
from pagina_mostrar_ids import pagina_mostrar_ids

def main():
    root = tk.Tk()
    root.title("Sistema de Gerenciamento de Instituição")
    root.geometry("1024x768")

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

    def show_page(page, *args):
        for widget in frame_content.winfo_children():
            widget.destroy()
        page(frame_content, *args)

    buttons = [
        ("Cadastro de Instituição", lambda: show_page(pagina1)),
        ("Estoque da Instituição", lambda: show_page(pagina_estoque)),
        ("Cadastro de Usuário", lambda: show_page(pagina2)),
        ("Produtos na Enfermaria", lambda: show_page(pagina3)),
        ("Cadastro de Quartos", lambda: show_page(pagina4)),
        ("Pesquisa de Usuários", lambda: show_page(pagina_pesquisa_usuario)),
        ("IDs de Usuários, Instituições e Enfermarias", lambda: show_page(pagina_mostrar_ids)),  # Novo botão adicionado
        ("Informações da Enfermaria", lambda: show_page(pagina_informacoes_enfermaria)),
        ("Editar Informações", lambda: show_page(pagina_editar_informacoes, 1))  # Ajuste para chamar função correta com ID do usuário
    ]

    for text, page in buttons:
        ttk.Button(scrollable_frame, text=text, command=page, style="TButton").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
