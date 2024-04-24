import pandas as pd
import numpy as np
import time

from SRC.utils import process_config


def main(vetorial_model, idf_df):
    print("Iniciando BUSCADOR em", time.strftime("%H:%M:%S"))
    print("Recebe como parâmetro o modelo vetorial e a matriz de idf")

    print("Lendo o arquivo de configuração: output consultas.csv do PC")
    config = process_config('SRC/BUSCADOR/BUSCADOR.CFG')

    print("Criando Dataframe para armazenar dados do arquivo de leitura")
    queries_df = pd.read_csv(config['CONSULTAS'], sep=';', dtype={'QueryNumber': str})

    print("Criando matriz para armazenar o modelo vetorial das queries")
    queries_vetorial_model = pd.DataFrame(0, index=vetorial_model.index, columns=queries_df['QueryNumber']
                                          .astype(str), dtype=float)

    print("Iterando sobre arquivo de leitura populando queries_vetorial_model")
    for index, row in queries_df.iterrows():
        # Itera sobre o texto da consulta
        for querie_term in row['QueryText'].split():
            # Verifica se o termo existe nas colunas de queries_vetorial_model
            if querie_term in queries_vetorial_model.index:
                if queries_vetorial_model.loc[querie_term, row['QueryNumber']] == 0:
                    # Soma 1 e multiplica pelo IDF do termo
                    queries_vetorial_model.loc[querie_term, row['QueryNumber']] += 1 * idf_df.loc[querie_term]

    print("Criando dataframe com as colunas 'QueryNumber' e a segunda uma lista ordenada pelo Ranking de "
          "'[Ranking, DocNumber, Distance]'")
    result_df = pd.DataFrame(columns=['QueryNumber', '[Ranking, DocNumber, Distance]'])

    print("Itera sobre as colunas de queries_vetorial_model para criar o resultado, isto é, para cada coluna de "
          "queries_vetorial_model, temos um querie_vector e calculamos a distâncias (ou similaridades) desse "
          "querie_vector para cada documento. Por fim, ordenamos essas similaridades e definimos o ranking para gerar o"
          " arquivo resultado com as colunas 'QueryNumber' e uma lista ordenada com '[Ranking, DocNumber, Distance]' "
          "de cada documento")
    for query_number in queries_vetorial_model.columns:
        # Define o vetor da consulta
        query_vector = queries_vetorial_model[query_number]

        # Cria um dicionário para armazenar as distâncias (ou similaridades) de cada documento {docNumber: distance}
        distance_dict = {}
        # Itera sobre as colunas de documentos de vetorial_model
        for doc_number, doc_column in vetorial_model.items():
            # Calcula a similaridade entre o vetor consulta e o dvetor documento
            similarity = np.dot(query_vector, doc_column) / (np.linalg.norm(query_vector) * np.linalg.norm(doc_column))
            # Armazena a similaridade do documento no dicionário distance_dict
            distance_dict[doc_number] = similarity

        # Ordena o dicionário por valores de similaridade em ordem decrescente
        sorted_distance = sorted(distance_dict.items(), key=lambda x: x[1], reverse=True)

        # Cria uma lista ordenada [Ranking, DocNumber, Distance] para cada documento
        sorted_list = [[rank, doc_number, distance] for rank, (doc_number, distance) in
                       enumerate(sorted_distance, start=1)]

        # Adiciona a lista ordenada ao result_df
        result_df.loc[len(result_df)] = [query_number, sorted_list]

    print("Gerando arquivo de output final: resultados.csv")
    result_df.to_csv(config['RESULTADOS'], sep=';', index=False)

    print("Finalizando BUSCADOR em", time.strftime("%H:%M:%S"))

if __name__ == "__main__":
    main()