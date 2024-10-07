# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
sns.set_style('whitegrid')
from bs4 import BeautifulSoup
from tqdm import tqdm
import sqlite3
from sqlalchemy import create_engine
import requests
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def get_content(site):
    resp = requests.get(site)
    return resp.text

# URL do site que você deseja acessar
site = "http://www.seagri.ba.gov.br/cotacao?produto=&praca=&tipo=&data_inicio=01/01/2015&data_final=31/12/2016"

# Chamada para obter o conteúdo da página
conteudo_pagina = get_content(site)

soup2 = BeautifulSoup(conteudo_pagina, 'html.parser')
div_page = soup2.find("tr", class_ ="odd")
div_page

# Suponha que 'conteudo_pagina' contenha o HTML da página

soup2 = BeautifulSoup(conteudo_pagina, 'html.parser')

# Encontrar todas as linhas com classes 'odd' e 'even'
linhas_odd = soup2.find_all("tr", class_="odd")
linhas_even = soup2.find_all("tr", class_="even")

# Criar uma lista para armazenar todos os resultados
resultados = []

# Função para extrair os dados de uma linha e adicionar aos resultados
def extrair_dados(linha):
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

# Iterar sobre as linhas ímpares (odd) e adicionar os resultados
for linha in linhas_odd:
    resultados.append(extrair_dados(linha))

# Iterar sobre as linhas pares (even) e adicionar os resultados
for linha in linhas_even:
    resultados.append(extrair_dados(linha))

# Exibir os resultados
for resultado in resultados:
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

# Salvar DataFrame no banco de dados
def save_to_db(df):
    with engine.connect() as connection:
        df.to_sql('database_agro', connection, if_exists='replace', index=False)
    print("Dados salvos no banco de dados SQLite!")

# Salvar o DataFrame no banco de dados
save_to_db(df)