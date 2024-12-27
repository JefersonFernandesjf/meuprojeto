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

def cadastrar_enfermaria(id_instituicao, nome):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO enfermaria (id_instituicao, nome)
                    VALUES (:1, :2)
                """
                cursor.execute(query, [id_instituicao, nome])
                connection.commit()
                messagebox.showinfo("Sucesso", "Enfermaria cadastrada com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar enfermaria: {e}")
        return False

def carregar_usuarios():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario, nome FROM usuarios")
                return cursor.fetchall()
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao carregar usuários: {e}")
        return []

def carregar_medicamentos():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_medicamento, nome FROM medicamentos")
                return cursor.fetchall()
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao carregar medicamentos: {e}")
        return []

def carregar_enfermarias():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_enfermaria, nome FROM enfermaria")
                return cursor.fetchall()
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao carregar enfermarias: {e}")
        return []

def cadastrar_medicamento(id_usuario, id_medicamento, id_enfermaria, hora_administrada, hora_proxima_dose):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO medicamentos_enfermaria (id_usuario, id_medicamento, id_enfermaria, hora_administrada, hora_proxima_dose, data_registro)
                    VALUES (:1, :2, :3, TO_DATE(:4, 'HH24:MI'), TO_DATE(:5, 'HH24:MI'), SYSDATE)
                """
                cursor.execute(query, [id_usuario, id_medicamento, id_enfermaria, hora_administrada, hora_proxima_dose])
                connection.commit()
                messagebox.showinfo("Sucesso", "Medicamento cadastrado com sucesso!")
                return True
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar medicamento: {e}")
        return False

def abrir_popup_usuario(parent):
    popup = tk.Toplevel(parent)
    popup.title("Selecionar Usuário")
    popup.geometry("400x300")
    usuarios = carregar_usuarios()
    usuarios_nomes = [f"{id_usuario}: {nome}" for id_usuario, nome in usuarios]
    selected_usuario = tk.StringVar(value=usuarios_nomes[0] if usuarios_nomes else "")

    ttk.Label(popup, text="Selecione o Usuário:", font=FONT).pack(padx=20, pady=10)
    usuario_menu = ttk.Combobox(popup, textvariable=selected_usuario, values=usuarios_nomes, state="readonly", font=FONT)
    usuario_menu.pack(padx=20, pady=10)

    def selecionar_usuario():
        popup.destroy()
        abrir_formulario_medicamento(parent, selected_usuario.get().split(":")[0])

    ttk.Button(popup, text="Selecionar", command=selecionar_usuario).pack(pady=10)

def abrir_formulario_medicamento(parent, id_usuario):
    popup = tk.Toplevel(parent)
    popup.title("Cadastrar Medicamento")
    popup.geometry("600x400")

    ttk.Label(popup, text="Medicamento:", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="e")

    medicamentos = carregar_medicamentos()
    medicamentos_nomes = [f"{id_med}: {nome}" for id_med, nome in medicamentos]
    selected_medicamento = tk.StringVar(value=medicamentos_nomes[0] if medicamentos_nomes else "")

    medicamento_menu = ttk.Combobox(popup, textvariable=selected_medicamento, values=medicamentos_nomes, state="readonly", font=FONT)
    medicamento_menu.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(popup, text="Hora Administrada (HH:MM):", font=FONT).grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_hora_administrada = ttk.Entry(popup, width=30, font=FONT)
    entry_hora_administrada.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(popup, text="Hora para Próxima Dose (HH:MM):", font=FONT).grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_hora_proxima_dose = ttk.Entry(popup, width=30, font=FONT)
    entry_hora_proxima_dose.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    ttk.Label(popup, text="Enfermaria:", font=FONT).grid(row=3, column=0, padx=20, pady=10, sticky="e")

    enfermarias = carregar_enfermarias()
    enfermarias_nomes = [f"{id_enf}: {nome}" for id_enf, nome in enfermarias]
    selected_enfermaria = tk.StringVar(value=enfermarias_nomes[0] if enfermarias_nomes else "")

    enfermaria_menu = ttk.Combobox(popup, textvariable=selected_enfermaria, values=enfermarias_nomes, state="readonly", font=FONT)
    enfermaria_menu.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    def cadastrar():
        medicamento_selecionado = selected_medicamento.get().split(":")[0]
        enfermaria_selecionada = selected_enfermaria.get().split(":")[0]
        hora_administrada = entry_hora_administrada.get()
        hora_proxima_dose = entry_hora_proxima_dose.get()

        if cadastrar_medicamento(id_usuario, medicamento_selecionado, enfermaria_selecionada, hora_administrada, hora_proxima_dose):
            entry_hora_administrada.delete(0, tk.END)
            entry_hora_proxima_dose.delete(0, tk.END)

    ttk.Button(popup, text="Cadastrar Medicamento", command=cadastrar).grid(row=4, column=0, columnspan=2, pady=10)

def abrir_popup_enfermaria(parent):
    popup = tk.Toplevel(parent)
    popup.title("Cadastrar Enfermaria")
    popup.geometry("400x300")

    ttk.Label(popup, text="Selecione a Instituição:", font=FONT).pack(padx=20, pady=10)

    instituicoes = carregar_instituicoes()
    instituicoes_nomes = [f"{id_inst}: {nome}" for id_inst, nome in instituicoes]
    selected_instituicao = tk.StringVar(value=instituicoes_nomes[0] if instituicoes_nomes else "")

    instituicao_menu = ttk.Combobox(popup, textvariable=selected_instituicao, values=instituicoes_nomes, state="readonly", font=FONT)
    instituicao_menu.pack(padx=20, pady=10)

    ttk.Label(popup, text="Nome da Enfermaria:", font=FONT).pack(padx=20, pady=10)
    entry_nome_enfermaria = ttk.Entry(popup, width=30, font=FONT)
    entry_nome_enfermaria.pack(padx=20, pady=10)

    def cadastrar_enf():
        instituicao_selecionada = selected_instituicao.get().split(":")[0]
        nome_enfermaria = entry_nome_enfermaria.get()

        if cadastrar_enfermaria(instituicao_selecionada, nome_enfermaria):
            entry_nome_enfermaria.delete(0, tk.END)

    ttk.Button(popup, text="Cadastrar Enfermaria", command=cadastrar_enf).pack(pady=10)

def pagina_enfermaria(parent):
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

    ttk.Label(scrollable_frame, text="Cadastro de Enfermaria e Medicamentos", font=FONT).grid(row=0, column=0, padx=20, pady=10, sticky="w")

    ttk.Button(scrollable_frame, text="Cadastrar Enfermaria", command=lambda: abrir_popup_enfermaria(parent)).grid(row=1, column=0, padx=20, pady=10)
    ttk.Button(scrollable_frame, text="Selecionar Usuário", command=lambda: abrir_popup_usuario(parent)).grid(row=2, column=0, padx=20, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gerenciamento de Enfermarias e Medicamentos")
    pagina_enfermaria(root)
    root.mainloop()
