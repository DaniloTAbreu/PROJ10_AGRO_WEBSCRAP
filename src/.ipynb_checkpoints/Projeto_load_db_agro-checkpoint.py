# Imports
import sqlite3
import pandas as pd

def load_from_db(db_name='my_database.db'):
    # Conectar ao banco de dados
    with sqlite3.connect(db_name) as conn:
        # Ler a tabela como um DataFrame
        df = pd.read_sql('SELECT * FROM my_table', conn)
        print("Dados carregados do banco de dados com sucesso.")
    return df

# Exemplo de uso
if __name__ == "__main__":
    # Carregar os dados do banco de dados
    df = load_from_db()
    print(df)