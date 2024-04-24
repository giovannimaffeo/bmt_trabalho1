import xml.etree.ElementTree as ET
import pandas as pd
import unicodedata
import time

from SRC.utils import process_config


def main():
    print("Iniciando PC em", time.strftime("%H:%M:%S"))

    def remove_semicolon(filename):
        print("Removendo ';' do arquivo XML:", filename)
        with open(filename, 'r') as file:
            data = file.read()
            data = data.replace(';', '')
        with open(filename, 'w') as file:
            file.write(data)

    print("Lendo o arquivo de configuração")
    config = process_config('./PC/PC.CFG')

    remove_semicolon(config['LEIA'])

    print("Carregando o arquivo XML")
    tree = ET.parse(config['LEIA'])
    root = tree.getroot()

    def process_query(query_text):
        print("Remover acentos e converter para maiúsculas:", query_text)
        query_text = ''.join(c for c in unicodedata.normalize('NFD', query_text) if unicodedata.category(c) != 'Mn')
        query_text = query_text.upper()
        return query_text

    query_numbers = []
    query_texts = []

    for query in root.findall('.//QUERY'):
        query_number = query.find('QueryNumber').text
        query_text = query.find('QueryText').text

        query_numbers.append(query_number)
        query_texts.append(query_text)

    df = pd.DataFrame({'QueryNumber': query_numbers, 'QueryText': query_texts})

    df['QueryText'] = df['QueryText'].apply(process_query)

    print("Gerando arquivo CSV")
    df.to_csv(config['CONSULTAS'], sep=';', index=False)

    query_numbers = []
    doc_numbers = []
    doc_votes = []

    for query in root.findall('.//QUERY'):
        query_number = query.find('QueryNumber').text

        for record in query.findall('.//Records/Item'):
            doc_number = record.text
            score = record.attrib['score']

            num_votes = 0
            for digit in score:
                if digit in ['1', '2']:
                    num_votes += 1

            query_numbers.append(query_number)
            doc_numbers.append(doc_number)
            doc_votes.append(num_votes)

    df = pd.DataFrame({'QueryNumber': query_numbers, 'DocNumber': doc_numbers, 'DocVotes': doc_votes})

    print("Escrevendo DataFrame em um arquivo CSV")
    df.to_csv(config['ESPERADOS'], sep=';', index=False)

    print("Finalizando PC em", time.strftime("%H:%M:%S"))

if __name__ == "__main__":
    main()