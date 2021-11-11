import pandas as pd
import pyodbc
import requests


def get_connection():
    #server = '10.0.0.50'
    server = 'localhost\\SQLEXPRESS'
    database = 'QSELECAO_BINARIOS'
    username = 'stevillis'
    password = '123456'

    connection = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return connection


def get_cursor(connection):
    cursor = connection.cursor()
    return cursor


def download_pdf(url):
    response = requests.get(url)
    return pyodbc.Binary(response.content)


def get_file_extension(path):
    return path.split('.')[-1]


def get_file_name(path, with_extension=False):
    firstpos = path.rfind("\\")
    if with_extension:
        lastpos = len(path)
    else:
        lastpos = path.rfind(".")
    return path[firstpos + 1:lastpos]


def read_excel(file):
    df = pd.read_excel(file, index_col=None, header=None)

    inscricoes = df[1]
    documentos = df[2]

    for count, i in enumerate(range(len(df))):
        if count > 0:
            inscricao = int(inscricoes[i])
            documento = documentos[i]

            insert_database_row(inscricao, documento)


def insert_database_row(inscricao, path_arquivo):
    nome_arquivo = str(inscricao) + '.' + get_file_extension(path_arquivo)

    # with open(path_arquivo, 'rb') as f:
    #    bindata = f.read()
    bindata = download_pdf(path_arquivo)

    params = (
        inscricao,  # existing COD_CONTEUDO_BINARIO
        8,  # tipo_conteudo
        inscricao,  # cod_conteudo
        nome_arquivo,  # nome_arquivo
        bindata,  # conteudo_binario
        0,  # compactado
    )

    connection = get_connection()
    cursor = get_cursor(connection)

    try:
        cursor.execute('''
            BEGIN
                IF NOT EXISTS (
                    SELECT COD_CONTEUDO_BINARIO FROM [dbo].[FW_CONTEUDOS_BINARIOS]
                    WHERE COD_CONTEUDO_BINARIO=?
                )
                BEGIN
                INSERT INTO [dbo].[FW_CONTEUDOS_BINARIOS]
                (TIPO_CONTEUDO_BINARIO, COD_CONTEUDO_BINARIO, NOME_ARQUIVO, CONTEUDO_BINARIO, COMPACTADO)
                VALUES
                (?, ?, ?, ?, ?)
                END
            END''', params)

        connection.commit()
    except pyodbc.IntegrityError as ie:
        print(ie)
    finally:
        connection.close()


def read_database_row():
    pass


read_excel('candidatos.xlsx')

# download_pdf('http://www.africau.edu/images/default/sample.pdf')
