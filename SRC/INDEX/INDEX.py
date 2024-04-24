import pandas as pd
import numpy as np
import re
import ast
import time

from SRC.utils import process_config


def main():
    print("Iniciando INDEX em", time.strftime("%H:%M:%S"))

    # Função para converter uma palavra para letras maiúsculas e remover caracteres não alfabéticos
    def clean_word(word):
        # Remove caracteres não alfabéticos e converte para maiúsculas
        cleaned_word = re.sub(r'[^a-zA-Z]', '', word).upper()
        return cleaned_word

    print("Lendo o arquivo de configuração: output escreva.csv do GLI")
    config = process_config('SRC/INDEX/INDEX.CFG')

    print("Criando matriz termo documento, onde aij é o número de registros do termo i no documento j")
    term_document_matrix = {}

    print("Iterando sobre arquivo de leitura e populando matriz termo documento")
    df = pd.read_csv(config['LEIA'], sep=';')
    for index, row in df.iterrows():
        # Se a palavra for válida
        if (pd.notna(row['ProcessedWord']) and all(char.isalpha() for char in row['ProcessedWord']) and
                len(row['ProcessedWord']) >= 2):
            processed_word = clean_word(row['ProcessedWord'])
            # Convertendo a string de RecordNumbers para uma lista
            record_numbers = ast.literal_eval(row['RecordNumbers'])

            if processed_word not in term_document_matrix:
                term_document_matrix[processed_word] = {}

            # Iterar sobre os identificadores de documentos
            for doc_number in record_numbers:
                # Atualizar a contagem de ocorrências da palavra no documento
                term_document_matrix[processed_word][doc_number] = (term_document_matrix[processed_word].get(doc_number
                                                                                                             , 0) + 1)

    print("Convertendo a matriz termo documento em um DataFrame")
    term_document_df = pd.DataFrame.from_dict(term_document_matrix, orient='index')
    term_document_df.fillna(0, inplace=True)

    print("Calculando a matriz Term Frequency (TF) a partir da matriz termo documento, onde aij é o TF do termo i no "
          "documento j e é dado por frequência do termo no documento dividido pela maior frequência no documento")
    # Calcula o máximo de cada coluna (documento)
    max_frquences = term_document_df.max()
    # Divide cada valor pelo máximo da coluna correspondente
    tf_df = term_document_df.div(max_frquences, axis=1)

    print("Calculando a matriz Inverse Document Frequency (IDF) a partir da matriz termo documento, onde cada elemento "
          "corresponde ao IDF de cada termo dado por: log ( número de documentos no conjunto / número de documentos que"
          " contém o termo")
    # Número total de documentos
    total_docs = len(term_document_df.columns)
    # Número de documentos que contêm cada termo
    docs_containing_term = term_document_df.astype(bool).sum(axis=1)
    idf_df = np.log10(total_docs / (docs_containing_term))

    print("Criando DataFrame de TF-IDF a partir da multiplicação de TF por IDF")
    tf_idf_df = tf_df.copy()  # Cria uma cópia do DataFrame tf_df para tf_idf_df
    for i in range(len(idf_df.values)):
        # Multiplica cada linha do DataFrame tf_idf_df pelo valor de IDF correspondente
        tf_idf_df.iloc[i] *= idf_df.values[i]

    print("Retornando estrutura que armazena TF-IDF para uso posterior pelo BUSCADOR")
    print("Finalizando INDEX em", time.strftime("%H:%M:%S"))

    return tf_idf_df, idf_df

if __name__ == "__main__":
    main()