import sqlite3
from datetime import datetime

# Nome do arquivo do banco de dados
DB_FILE = 'cotacoes.db'

def setup_database():
    """
    Configura o banco de dados SQLite e cria a tabela 'cotacoes' se ela não existir.
    A tabela armazena a cotação do dólar e a data da última atualização.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Cria a tabela 'cotacoes'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotacoes (
                moeda TEXT PRIMARY KEY,
                valor REAL,
                data_atualizacao TEXT
            )
        ''')

        conn.commit()
        print("Banco de dados configurado com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro ao conectar ou configurar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def save_cotacao(moeda, valor):
    """Salva uma cotação no banco de dados."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT OR REPLACE INTO cotacoes (moeda, valor, data_atualizacao)
            VALUES (?, ?, ?)
        ''', (moeda, valor, data_hora))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao salvar a cotação: {e}")
    finally:
        if conn:
            conn.close()

def get_cotacao(moeda):
    """Lê a última cotação salva do banco de dados."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT valor, data_atualizacao FROM cotacoes WHERE moeda = ?", (moeda,))
        cotacao = cursor.fetchone()
        return cotacao
    except sqlite3.Error as e:
        print(f"Erro ao ler a cotação: {e}")
        return None
    finally:
        if conn:
            conn.close()
