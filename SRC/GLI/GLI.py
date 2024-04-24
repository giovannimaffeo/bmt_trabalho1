import xml.etree.ElementTree as ET
import pandas as pd
import unicodedata
import time

from SRC.utils import process_config


def process_word(word):
    print("Remover acentos e caracteres especiais:", word)
    normalized_word = ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn' and c.isalnum())
    print("Converter para maiúsculas:", normalized_word)
    processed_word = normalized_word.upper()
    return processed_word

def main():
    print("Iniciando GLI em", time.strftime("%H:%M:%S"))

    # Ler o arquivo de configuração
    config = process_config('GLI/GLI.CFG')

    print("Listas para armazenar os dados")
    # Listas para armazenar os dados
    words_dict = {}

    print("Iterar sobre arquivos de leitura")
    # Iterar sobre arquivos de leitura
    for file in config['LEIA']:
        # Carregar o arquivo XML
        tree = ET.parse(file)
        root = tree.getroot()

        print("Iterar sobre os registros no arquivo XML")
        # Iterar sobre os registros no arquivo XML
        for record in root.findall('.//RECORD'):
            record_num = int(record.find('RECORDNUM').text.strip())
            title = record.find('TITLE').text

            print("Extrair palavras do campo ABSTRACT")
            # Extrair palavras do campo ABSTRACT
            abstract = record.find('ABSTRACT')
            if abstract is not None:
                text = abstract.text
            else:
                print("Se ABSTRACT não existir, extrair palavras do campo EXTRACT se existir")
                # Se ABSTRACT não existir, extrair palavras do campo EXTRACT se existir
                extract = record.find('EXTRACT')
                if extract is not None:
                    text = extract.text
                else:
                    continue

            print("Iterar sobre palavras extraídas")
            # Iterar sobre palavras extraídas
            words = text.split()
            for word in words:
                print("Processar palavra")
                # Processar palavra
                processed_word = process_word(word)
                print("Adicionar palavra ao dicionário")
                # Adicionar palavra ao dicionário
                if processed_word in words_dict:
                    words_dict[processed_word].append(record_num)
                else:
                    words_dict[processed_word] = [record_num]

    print("Criar o DataFrame")
    # Criar o DataFrame
    df = pd.DataFrame({'ProcessedWord': list(words_dict.keys()), 'RecordNumbers': list(words_dict.values())})

    print("Gerar arquivo CSV")
    # Gerar arquivo CSV
    df.to_csv(config['ESCREVA'], sep=';', index=False)

    print("Finalizando GLI em", time.strftime("%H:%M:%S"))

if __name__ == "__main__":
    main()