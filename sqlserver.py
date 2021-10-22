import pandas as pd
import pyodbc
import requests

"""
for row in cursor.fetchall():
    print(row)
"""


def get_connection():
    # SERVER = '10.0.0.50'
    server = 'localhost\\SQLEXPRESS'
    database = 'QSELECAO_BINARIOS'
    # USERNAME = 'stevillis'
    username = 'sa'
    # PASSWORD = '123456@@'
    password = '123456'

    connection = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return connection


def get_cursor(connection):
    cursor = connection.cursor()
    return cursor


def download_pdf(url):
    response = requests.get(url)
    print(pyodbc.Binary(response.content))


def read_excel(file_path):
    df = pd.read_excel(file_path, index_col=None, header=None)
    print(df['Nome'])


def insert_row():
    file_name = 'sample.pdf'
    file = '' + file_name

    with open(file, 'rb') as f:
        bindata = f.read()

    params = (
        2,  # existing COD_CONTEUDO_BINARIO
        2,  # cod_conteudo
        1,  # tipo_conteudo
        file_name,  # nome_arquivo
        bindata,  # conteudo_binario
        1,  # compactado
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


def read_row():
    pass


read_excel('candidatos.xlsx')
# insert_row()


# download_pdf('http://www.africau.edu/images/default/sample.pdf')
