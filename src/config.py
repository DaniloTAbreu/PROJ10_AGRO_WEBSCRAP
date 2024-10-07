# config.py
import os

# Configurações para o scraper
SCRAPER_CONFIG = {
    'base_url': 'http://www.seagri.ba.gov.br/cotacao',
    'params': {
        'produto': '',
        'praca': '',
        'tipo': '',
        'data_inicio': '01/01/2015',
        'data_final': '31/12/2016',
        'pagina': 1  # Padrão para a primeira página
    },
    'max_paginas': 150
}

# Configurações para o banco de dados
DATABASE_CONFIG = {
    'db_name': os.path.join(r'C:\Users\Danilo\PROJETOS\PROJETO12_TESTE_WEBSCRAPPING_AGRO\data\raw_processed', 'database_agro.db'),
    'table_name': 'database_agro'
}


# Configurações para o arquivo CSV
CSV_CONFIG = {
    'caminho_arquivo_csv': r'C:\Users\Danilo\PROJETOS\PROJETO12_TESTE_WEBSCRAPPING_AGRO\data\raw_processed\dados_agro.csv'
}
