import tkinter as tk
from tkinter import ttk
from db_config import conectar_bd
import cx_Oracle

FONT = ("Arial", 14)

def cadastrar_quarto(numero_quarto, estado_quarto, id_usuario):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO quartos (numero_quarto, estado_quarto, id_usuario)
                    VALUES (:1, :2, :3)
                """
                cursor.execute(query, [numero_quarto, estado_quarto, id_usuario])
                connection.commit()
                return True
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao cadastrar quarto: {e}")
        return False

def pagina4(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Número do Quarto:", font=FONT).grid(row=0, column=0, padx=20, pady=10)
    entry_numero_quarto = tk.Entry(frame, width=30, font=FONT)
    entry_numero_quarto.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(frame, text="Estado do Quarto:", font=FONT).grid(row=1, column=0, padx=20, pady=10)
    entry_estado_quarto = tk.Entry(frame, width=30, font=FONT)
    entry_estado_quarto.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(frame, text="ID do Usuário:", font=FONT).grid(row=2, column=0, padx=20, pady=10)
    entry_id_usuario = tk.Entry(frame, width=30, font=FONT)
    entry_id_usuario.grid(row=2, column=1, padx=20, pady=10)

    def cadastrar():
        numero_quarto = entry_numero_quarto.get()
        estado_quarto = entry_estado_quarto.get()
        id_usuario = entry_id_usuario.get()

        if not cadastrar_quarto(numero_quarto, estado_quarto, id_usuario):
            print("Erro ao cadastrar quarto.")
    
    tk.Button(frame, text="Cadastrar Quarto", font=FONT, command=cadastrar).grid(row=3, column=0, columnspan=2, pady=10)

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    pagina4(root)
    root.mainloop()
