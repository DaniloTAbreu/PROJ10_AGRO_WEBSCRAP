# parser.py

import sqlite3
import pandas as pd
from .config import DATABASE_CONFIG

def load_from_db():
    db_name = DATABASE_CONFIG['db_name']
    table_name = DATABASE_CONFIG['table_name']
    
    try:
        # Conectar ao banco de dados
        with sqlite3.connect(db_name) as conn:
            # Ler a tabela como um DataFrame
            query = f'SELECT * FROM {table_name}'  
            df = pd.read_sql(query, conn)
            print("Dados carregados do banco de dados com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        df = pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
    return df

# Exemplo de uso
if __name__ == "__main__":
    # Carregar os dados do banco de dados
    df = load_from_db()
    print(df.head())
