import xml.etree.ElementTree as ET
import pandas as pd
import unicodedata

from utils import process_config


# Função para remover os ";" do arquivo XML
def remove_semicolon(filename):
    with open(filename, 'r') as file:
        data = file.read()
        data = data.replace(';', '')
    with open(filename, 'w') as file:
        file.write(data)

# Ler o arquivo de configuração
config = process_config('PC.CFG')

# Remover ";" do arquivo XML
remove_semicolon(config['LEIA'])

# Carregar o arquivo XML
tree = ET.parse(config['LEIA'])
root = tree.getroot()

# ------------------------------------------------------- GERAR PRIMEIRO ARQUIVO

# Função para remover acentos e converter para maiúsculas
def process_query(query_text):
    # Remover acentos
    query_text = ''.join(c for c in unicodedata.normalize('NFD', query_text) if unicodedata.category(c) != 'Mn')
    # Converter para maiúsculas
    query_text = query_text.upper()
    return query_text

# Listas para armazenar os dados
query_numbers = []
query_texts = []

# Iterar sobre os elementos QUERY dentro de FILEQUERY
for query in root.findall('.//QUERY'):
    query_number = query.find('QueryNumber').text
    query_text = query.find('QueryText').text

    query_numbers.append(query_number)
    query_texts.append(query_text)

# Criar o DataFrame
df = pd.DataFrame({'QueryNumber': query_numbers, 'QueryText': query_texts})

# Processar QueryText
df['QueryText'] = df['QueryText'].apply(process_query)

# Gerar arquivo CSV
df.to_csv(config['CONSULTAS'], sep=';', index=False)

# ------------------------------------------------------- GERAR SEGUNDO ARQUIVO

# Listas para armazenar os dados
query_numbers = []
doc_numbers = []
doc_votes = []

# Iterar sobre os elementos QUERY dentro de FILEQUERY
for query in root.findall('.//QUERY'):
    query_number = query.find('QueryNumber').text

    # Iterar sobre os elementos Item dentro de Records
    for record in query.findall('.//Records/Item'):
        doc_number = record.text
        score = record.attrib['score']

        # Calcular o número de votos para o documento
        num_votes = 0
        for digit in score:
            if digit in ['1', '2']:
                num_votes += 1

        # Adicionar os dados às listas
        query_numbers.append(query_number)
        doc_numbers.append(doc_number)
        doc_votes.append(num_votes)

# Criar DataFrame
df = pd.DataFrame({'QueryNumber': query_numbers, 'DocNumber': doc_numbers, 'DocVotes': doc_votes})

# Escrever DataFrame em um arquivo CSV
df.to_csv(config['ESPERADOS'], sep=';', index=False)
