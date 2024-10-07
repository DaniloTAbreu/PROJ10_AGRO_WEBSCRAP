# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import sqlite3
from sqlalchemy import create_engine
import warnings

# Configurações
sns.set_style('whitegrid')
warnings.filterwarnings("ignore", category=FutureWarning)

# Função para obter o conteúdo da página
def get_content(site):
    try:
        response = requests.get(site)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao acessar {site}: {e}")
        return None

# Função para extrair dados de uma linha da tabela
def extrair_dados(linha):
    try:
        data = linha.find("td", class_="active").text.strip()
        produto = linha.find_all("td")[1].text.strip()
        municipio = linha.find_all("td")[2].text.strip()
        tipo = linha.find_all("td")[3].text.strip()
        peso = linha.find_all("td")[4].text.strip()
        preco = linha.find_all("td")[5].text.strip()
        return {
            "data": data,
            "produto": produto,
            "municipio": municipio,
            "tipo": tipo,
            "peso": peso,
            "preco": preco
        }
    except IndexError:
        print("Erro ao extrair dados de uma linha.")
        return None

# URL base e parâmetros de consulta
base_url = "http://www.seagri.ba.gov.br/cotacao"
params = {
    'produto': '',
    'praca': '',
    'tipo': '',
    'data_inicio': '01/01/2015',
    'data_final': '31/12/2016',
    'pagina': 1  # Padrão para a primeira página
}

# Criar uma lista para armazenar todos os resultados
resultados = []

# Defina o número máximo de páginas a serem iteradas (ajuste conforme necessário)
max_paginas = 150

for pagina in tqdm(range(1, max_paginas + 1), desc='Iterando pelas páginas'):
    params['pagina'] = pagina
    site = requests.Request('GET', base_url, params=params).prepare().url
    conteudo_pagina = get_content(site)
    
    if conteudo_pagina is None:
        continue  # Pular página se houver erro no acesso

    soup = BeautifulSoup(conteudo_pagina, 'html.parser')

    # Encontrar todas as linhas com classes 'odd' e 'even'
    linhas_odd = soup.find_all("tr", class_="odd")
    linhas_even = soup.find_all("tr", class_="even")

    # Iterar sobre as linhas ímpares (odd) e pares (even) e adicionar os resultados
    for linha in linhas_odd + linhas_even:
        dados = extrair_dados(linha)
        if dados:
            resultados.append(dados)

# Exibir os resultados (opcional, para depuração)
for resultado in resultados[:5]:  # Exibir apenas os primeiros 5 resultados para verificar
    print(f"Data: {resultado['data']}")
    print(f"Produto: {resultado['produto']}")
    print(f"Município: {resultado['municipio']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"Peso: {resultado['peso']}")
    print(f"Preco: {resultado['preco']}")
    print()  # linha em branco para separar cada conjunto de dados

# Criando o DataFrame
df = pd.DataFrame(resultados)

# Defina a URL de conexão para SQLite
db_url = 'sqlite:///database_agro.db'

# Crie um engine de conexão
engine = create_engine(db_url)

# Função para salvar o DataFrame no banco de dados
def save_to_db(df):
    try:
        with engine.connect() as connection:
            df.to_sql('database_agro', connection, if_exists='replace', index=False)
        print("Dados salvos no banco de dados SQLite!")
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")

# Salvar o DataFrame no banco de dados
save_to_db(df)
