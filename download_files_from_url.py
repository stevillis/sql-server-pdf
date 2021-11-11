import re

import pandas as pd
import requests


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def get_file_extension(path):
    return path.split('.')[-1]


def download_pdf(inscricao, url):
    response = requests.get(url)
    filename = get_filename_from_cd(response.headers.get('content-disposition'))
    extension = None
    if filename is None:
        if url.find('/'):
            filename_from_url = url.rsplit('/', 1)[1]
            extension = get_file_extension(filename_from_url)
    else:
        extension = get_file_extension(filename)

    nome_arquivo = inscricao
    if extension:
        nome_arquivo += '.' + extension

    open('./dst/' + nome_arquivo, 'wb').write(response.content)


def read_excel(file):
    df = pd.read_excel(file, index_col=None, header=None)

    inscricoes = df[2]
    documentos = df[3]

    for count, i in enumerate(range(len(df))):
        if count > 0:
            inscricao = str(inscricoes[i])
            url = documentos[i]

            download_pdf(inscricao, url)


read_excel('candidatos.xlsx')

# download_pdf('http://www.africau.edu/images/default/sample.pdf')
