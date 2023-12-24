import glob

import pandas as pd
import os

# getting all the csv files from the folder and subfolders
files = glob.glob('exports/*.csv', recursive=True)

col_names = ['CNPJ', 'Razão Social', 'Data da Abertura', 'Porte', 'Natureza Jurídica', 'Opção pelo MEI',
                                 'Opção pelo Simples', 'Tipo', 'Situação', 'Data Situação Cadastral',
                                 'Logradouro', 'Bairro', 'CEP', 'Município', 'Estado', 'Para correspondência']

# creating a dataframe with the column names
df = pd.DataFrame(columns=col_names)

# iterating through all the csv files
for file in files:
    # reading the csv file
    df1 = pd.read_csv(file, names=col_names)
    print(file)
    # appending the data to the dataframe
    df = df.append(df1, ignore_index=True)

# removing the duplicates based on third column
df = df.drop_duplicates(subset='CNPJ')

# removing the rows whose Natureza Jurídica is not Ativa
df = df[df['Natureza Jurídica'] == 'Ativa']




# exporting the combined dataframe into a csv file
df.to_csv('combineddata2.csv', index=False)

