# tests/test_scraper.py
 
import pytest
import pandas as pd
from src.scraper import get_content

def test_scrape_data_valid_url():
    url = "http://www.seagri.ba.gov.br/cotacao"
    df = get_content(url)
    
    # Defina o DataFrame esperado com dados fictícios de acordo com o formato real esperado
    expected_data = {
        'data': ['01/01/2015'],
        'produto': ['Produto1'],  # Exemplo de dados esperados
        'municipio': ['municipio1'],
        'tipo': ['Tipo1', 'Tipo2'],
        'peso': ['cx 30 Kg'],
        'preco': ['R$ 100,00'],
            }
    expected_df = pd.DataFrame(expected_data)
    
    # Compare o DataFrame resultante com o esperado
    pd.testing.assert_frame_equal(df, expected_df)

def test_scrape_data_invalid_url():
    url = "http://www.seagri.ba.gov.br/invalid"
    with pytest.raises(ValueError):
        get_content(url)

# Adicione mais testes conforme necessário
