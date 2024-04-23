import xml.etree.ElementTree as ET
import pandas as pd
import unicodedata

from utils import process_config


# Função para remover acentos e converter para maiúsculas
def process_word(word):
    # Remover acentos e caracteres especiais
    normalized_word = ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn' and c.isalnum())
    # Converter para maiúsculas
    processed_word = normalized_word.upper()
    return processed_word

# Ler o arquivo de configuração
config = process_config('GLI.CFG')

# Listas para armazenar os dados
words_dict = {}

# Iterar sobre arquivos de leitura
for file in config['LEIA']:
    # Carregar o arquivo XML
    tree = ET.parse(file)
    root = tree.getroot()

    # Iterar sobre os registros no arquivo XML
    for record in root.findall('.//RECORD'):
        record_num = int(record.find('RECORDNUM').text.strip())
        title = record.find('TITLE').text

        # Extrair palavras do campo ABSTRACT
        abstract = record.find('ABSTRACT')
        if abstract is not None:
            text = abstract.text
        else:
            # Se ABSTRACT não existir, extrair palavras do campo EXTRACT se existir
            extract = record.find('EXTRACT')
            if extract is not None:
                text = extract.text
            else:
                continue

        # Iterar sobre palavras extraídas
        words = text.split()
        for word in words:
            # Processar palavra
            processed_word = process_word(word)
            # Adicionar palavra ao dicionário
            if processed_word in words_dict:
                words_dict[processed_word].append(record_num)
            else:
                words_dict[processed_word] = [record_num]

# Criar o DataFrame
df = pd.DataFrame({'ProcessedWord': list(words_dict.keys()), 'RecordNumbers': list(words_dict.values())})

# Gerar arquivo CSV
df.to_csv(config['ESCREVA'], sep=';', index=False)
