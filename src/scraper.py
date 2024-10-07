# scraper.py

import os
import pandas as pd
import requests
import seaborn as sns
import re
import warnings
import sqlite3
from bs4 import BeautifulSoup
from tqdm import tqdm
from sqlalchemy import create_engine
from config import SCRAPER_CONFIG, CSV_CONFIG, DATABASE_CONFIG

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
    'produto': '481',
    'praca': '',
    'tipo': '',
    'data_inicio': '01/01/2015',
    'data_final': '31/12/2023',
    'pagina': 1  # Padrão para a primeira página
}

# Criar uma lista para armazenar todos os resultados
resultados = []

# Defina o número máximo de páginas a serem iteradas (ajuste conforme necessário)
max_paginas = 82

for pagina in tqdm(range(1, max_paginas + 1), desc='Iterando pelas páginas'):
    if pagina == 1:
        # Para a primeira página, não adicionar o parâmetro 'page'
        site = f"{base_url}?produto={params['produto']}&praca={params['praca']}&tipo={params['tipo']}&data_inicio={params['data_inicio']}&data_final={params['data_final']}"
    else:
        # Para as demais páginas, adicionar o parâmetro 'page'
        site = f"{base_url}?page={pagina}&produto={params['produto']}&praca={params['praca']}&tipo={params['tipo']}&data_inicio={params['data_inicio']}&data_final={params['data_final']}"
    
    conteudo_pagina = get_content(site)

    if conteudo_pagina is None:
        continue  # Pular página se houver erro no acesso

    soup = BeautifulSoup(conteudo_pagina, 'html.parser')

    # Verifique se a página contém dados
    if not soup.find_all("tr", class_=["odd", "even"]):
        print(f"Nenhum dado encontrado na página {pagina}.")
        continue

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
db_name = r'C:\Users\Danilo\PROJETOS\PROJETO12_TESTE_WEBSCRAPPING_AGRO\data\raw\database_agro.db'

# Crie um engine de conexão
engine = create_engine(f'sqlite:///{db_name}', pool_pre_ping=True)

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

# Defina o caminho do arquivo CSV
caminho_arquivo_csv = r'C:\Users\Danilo\PROJETOS\PROJETO12_TESTE_WEBSCRAPPING_AGRO\data\raw\dados_agro.csv'

# Verificar se o diretório existe, se não, criar
os.makedirs(os.path.dirname(caminho_arquivo_csv), exist_ok=True)

# Salvar o DataFrame como um arquivo CSV
try:
    df.to_csv(caminho_arquivo_csv, index=False)
    print(f"Dados salvos em {caminho_arquivo_csv}!")
except Exception as e:
    print(f"Erro ao salvar os dados como CSV: {e}")