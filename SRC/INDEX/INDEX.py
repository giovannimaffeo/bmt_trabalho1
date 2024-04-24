import pandas as pd
import numpy as np
import re
import ast
import time

from utils import process_config

print("Iniciando INDEX em", time.strftime("%H:%M:%S"))

print("Função para converter uma palavra para letras maiúsculas e remover caracteres não alfabéticos")
# Função para converter uma palavra para letras maiúsculas e remover caracteres não alfabéticos
def clean_word(word):
    print("Remove caracteres não alfabéticos e converte para maiúsculas:", word)
    # Remove caracteres não alfabéticos e converte para maiúsculas
    cleaned_word = re.sub(r'[^a-zA-Z]', '', word).upper()
    return cleaned_word

# Ler o arquivo de configuração
print("Lendo o arquivo de configuração")
config = process_config('INDEX.CFG')

# Criar matriz termo documento
print("Criando matriz termo documento")
term_document_matrix = {}

# Iterar sobre arquivo de leitura
print("Iterando sobre arquivo de leitura")
df = pd.read_csv(config['LEIA'], sep=';')
for index, row in df.iterrows():
    # Se a palavra for válida
    if pd.notna(row['ProcessedWord']) and all(char.isalpha() for char in row['ProcessedWord']) and len(row['ProcessedWord']) >= 2:
        processed_word = clean_word(row['ProcessedWord'])
        # Convertendo a string de RecordNumbers para uma lista
        record_numbers = ast.literal_eval(row['RecordNumbers'])

        if processed_word not in term_document_matrix:
            term_document_matrix[processed_word] = {}

        # Iterar sobre os identificadores de documentos
        for doc_number in record_numbers:
            # Atualizar a contagem de ocorrências da palavra no documento
            term_document_matrix[processed_word][doc_number] = (term_document_matrix[processed_word].get(doc_number, 0)
                                                                + 1)

print("Convertendo a matriz termo documento em um DataFrame")
# Converter a matriz termo documento em um DataFrame
term_document_df = pd.DataFrame.from_dict(term_document_matrix, orient='index')
term_document_df.fillna(0, inplace=True)

# Calculando o Term Frequency (TF)
print("Calculando o Term Frequency (TF)")
tf = term_document_df.div(term_document_df.sum(axis=0), axis=1)

# Calculando o Inverse Document Frequency (IDF)
print("Calculando o Inverse Document Frequency (IDF)")
# Número total de documentos
total_docs = len(term_document_df.columns)
# Número de documentos que contêm cada termo
docs_containing_term = term_document_df.astype(bool).sum(axis=1)
idf = np.log(total_docs / (1 + docs_containing_term))

# Dataframe de TF-IDF
print("Criando DataFrame de TF-IDF")
tf_idf_rows = []
for i, row in tf.iterrows():
    tf_idf_row = row * idf[1]
    tf_idf_rows.append(tf_idf_row)
tf_idf_df = pd.DataFrame(tf_idf_rows)
tf_idf_df.columns = term_document_df.columns
tf_idf_df.index = term_document_df.index

print("Finalizando INDEX em", time.strftime("%H:%M:%S"))