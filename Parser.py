import hashlib
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from stack import appendLink, getLink, getLinksLength, deleteLink

maindf = pd.DataFrame(
    columns=['CNPJ', 'Razão Social', 'Data da Abertura', 'Porte', 'Natureza Jurídica', 'Opção pelo MEI',
             'Opção pelo Simples', 'Tipo', 'Situação', 'Data Situação Cadastral',
             'Logradouro', 'Bairro', 'CEP', 'Município', 'Estado', 'Para correspondência'])


def hashCaluculator(text):
    hash_object = hashlib.sha256(text.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def textParser(text):
    cnpj = ''
    social = ''
    data = ''
    natureza = ''
    situacao = ''
    capital = ''
    simples = ''
    tipo = ''
    porte = ''
    data_situacao = ''
    logradouro = ''
    bairro = ''
    cep = ''
    municipio = ''
    estado = ''
    para_correspond = ''
    # getting title of from post-title empresa-title class
    soup = BeautifulSoup(text, 'html.parser')
    hits = soup.find_all('h1', class_='post-title empresa-title')
    main_title = hits[0].text
    # getting all the links which has these classes 'btn btn-a btn-sm'
    # getting all the p tags of a div with class col-left
    hits = soup.find_all('div', class_='col-left')
    for hit in hits:
        for p in hit.find_all('p'):
            # getting all the text in the p tag
            text = p.text
            if 'CNPJ:' in text:
                cnpj = text.split('CNPJ:')[1].strip()
            if 'Razão Social:' in text:
                social = text.split('Razão Social:')[1].strip()
            if 'Data de Abertura:' in text:
                data = text.split('Data de Abertura:')[1].strip()
            if 'Natureza Jurídica:' in text:
                natureza = text.split('Natureza Jurídica:')[1].strip()
            if 'Situação:' in text:
                situacao = text.split('Situação:')[1].strip()
            if 'Opção pelo MEI:' in text:
                capital = text.split('Opção pelo MEI:')[1].strip()
            if 'Opção pelo Simples:' in text:
                simples = text.split('Opção pelo Simples:')[1].strip()
            if 'Tipo:' in text:
                tipo = text.split('Tipo:')[1].strip()
            if 'Porte:' in text:
                porte = text.split('Porte:')[1].strip()
            if 'Data Situação Cadastral:' in text:
                data_situacao = text.split('Data Situação Cadastral:')[1].strip()
            if 'Logradouro:' in text:
                logradouro = text.split('Logradouro:')[1].strip()
            if 'Bairro:' in text:
                bairro = text.split('Bairro:')[1].strip()
            if 'CEP:' in text:
                cep = text.split('CEP:')[1].strip()
            if 'Município:' in text:
                municipio = text.split('Município:')[1].strip()
            if 'Estado:' in text:
                estado = text.split('Estado:')[1].strip()
            if 'Para correspondência:' in text:
                para_correspond = text.split('Para correspondência:')[1].strip()

    df = pd.DataFrame(
        columns=['CNPJ', 'Razão Social', 'Data da Abertura', 'Porte', 'Natureza Jurídica', 'Opção pelo MEI',
                 'Opção pelo Simples', 'Tipo', 'Situação', 'Data Situação Cadastral',
                 'Logradouro', 'Bairro', 'CEP', 'Município', 'Estado', 'Para correspondência'])
    df.loc[len(df)] = [cnpj, social, data, natureza, situacao, capital, simples, tipo, porte, data_situacao,
                       logradouro, bairro, cep, municipio, estado, para_correspond]

    # checking if Nauterza Jurídica is Ativa or not
    if df['Natureza Jurídica'][0] != 'Ativa':
        return None
    nextLinks = soup.find_all('a', attrs={'class': 'btn btn-a btn-sm'})
    for link in nextLinks:
        appendLink('https://cnpj.biz' + link['href'])

    return df


def getProxy(file):
    # reading txt file containing proxies
    handler = open(file, 'r')
    proxies = handler.readlines()
    # removing \n from the end of each proxy
    for i in range(len(proxies)):
        proxies[i] = proxies[i][:-1]
    handler.close()
    return proxies


def getData(link, fileNo):
    global maindf
    req = requests.get(link)
    # discarding the link if it contains Contatos
    if 'Contatos' in req.text:
        return
    # parsing the text
    df = textParser(req.text)
    # concatenating the dataframes
    if df is None:
        return
    tempDF = pd.concat([maindf, df], ignore_index=True)
    tempDF.to_csv(f'exports/{fileNo}.csv', index=False)
    print("Saved the data to: ", f'exports/{fileNo}.csv')

j=1
i = 1
allLinks = []
newdf = pd.read_csv('combined.csv')
allLinks = newdf['col3'].tolist()
if __name__ == '__main__':
    for l in allLinks:
        print(j)
        j+=1

        link = l
        # req = requests.get(link)
        if getLinksLength() == 0:
            appendLink(link)
        while getLinksLength() > 0:
            link = getLink(i)
            print("Requesting for link: ", link)
            if len(link) > 0:
                getData(link[0][1], i)
                deleteLink(link[0][0])
            i += 1
