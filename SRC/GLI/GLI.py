import xml.etree.ElementTree as ET
import pandas as pd
import unicodedata
import time

from SRC.utils import process_config


def process_word(word):
    # Remover acentos e caracteres especiais
    normalized_word = ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn' and c.isalnum())
    # Converter para maiúsculas
    processed_word = normalized_word.upper()
    return processed_word

def main():
    print("Iniciando GLI em", time.strftime("%H:%M:%S"))

    print("Lendo o arquivo de configuração")
    config = process_config('SRC/GLI/GLI.CFG')

    print("Definindo dicionário para armazenar a palavra processada e o número de registros")
    words_dict = {}

    print("Iterar sobre arquivos de leitura e popular dicionário de palavras")
    # Iterar sobre arquivos de leitura
    for file in config['LEIA']:
        # Carregar o arquivo XML
        tree = ET.parse(file)
        root = tree.getroot()

        # Iterar sobre os registros no arquivo XML
        for record in root.findall('.//RECORD'):
            record_num = int(record.find('RECORDNUM').text.strip())

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

    print("Criar o DataFrame a partir do dicionário")
    # Criar o DataFrame
    df = pd.DataFrame({'ProcessedWord': list(words_dict.keys()), 'RecordNumbers': list(words_dict.values())})

    print("Gerando arquivo escreva.csv")
    df.to_csv(config['ESCREVA'], sep=';', index=False)

    print("Finalizando GLI em", time.strftime("%H:%M:%S"))

if __name__ == "__main__":
    main()