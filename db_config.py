import json
import cx_Oracle

def ler_configuracao():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        config = {
            "DB_USER": "SYSTEM",
            "DB_PASSWORD": "cloud1%",
            "DB_DSN": "localhost/XE"
        }
        salvar_configuracao(config)
        return config

def salvar_configuracao(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

# Função para conectar ao banco de dados
def conectar_bd():
    return cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN, encoding="UTF-8", nencoding="UTF-8")

# Carregando a configuração inicial
config = ler_configuracao()

DB_USER = config['DB_USER']
DB_PASSWORD = config['DB_PASSWORD']
DB_DSN = config['DB_DSN']
