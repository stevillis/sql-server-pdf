from os import listdir

import pyodbc
import requests


def get_connection():
    # server = '10.0.0.50'
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


def get_file_extension(path):
    return path.split('.')[-1]


def get_file_name(file):
    if file.find('_') > -1:
        return file.split('_')[0]
    return file.split('.')[0]


def log_erro(inscricao):
    with open('log_insert.txt', 'a') as file:
        file.write(inscricao + '\n')


def insert_database_row(inscricao, nome_arquivo, tipo_conteudo, conteudo_binario, compactado):
    params = (
        inscricao,  # existing COD_CONTEUDO_BINARIO
        tipo_conteudo,  # TIPO_CONTEUDO_BINARIO
        inscricao,  # COD_CONTEUDO_BINARIO
        nome_arquivo,  # NOME_ARQUIVO
        conteudo_binario,  # CONTEUDO_BINARIO
        compactado,  # COMPACTADO
    )

    connection = get_connection()
    cursor = get_cursor(connection)

    success = False
    try:
        cursor.execute('''
            BEGIN
                IF NOT EXISTS (
                    SELECT COD_CONTEUDO_BINARIO FROM [dbo].[FW_CONTEUDOS_BINARIOS]
                    WHERE COD_CONTEUDO_BINARIO = ?
                )
                BEGIN
                INSERT INTO [dbo].[FW_CONTEUDOS_BINARIOS]
                (TIPO_CONTEUDO_BINARIO, COD_CONTEUDO_BINARIO, NOME_ARQUIVO, CONTEUDO_BINARIO, COMPACTADO)
                VALUES
                (?, ?, ?, ?, ?)
                END
            END''', params)

        if cursor.rowcount > 0:
            connection.commit()
            success = True
        else:
            log_erro(inscricao)
            success = False
    except pyodbc.IntegrityError as ie:
        log_erro(inscricao)
        print(ie)
        success = False
    finally:
        connection.close()
        return success


def add_backslash(path):
    new_path = path
    if len(new_path) > 0:
        if new_path[-1] != '\\':
            new_path += '\\'
    return new_path


def read_directory():
    path_pdfs = input('Caminho dos Arquivos PDFs: ')
    path_pdfs = add_backslash(path_pdfs)
    return path_pdfs


def insert_pdfs():
    path_pdfs = read_directory()
    pdf_list = listdir(path_pdfs)

    files_located = len(pdf_list)
    pdfs_located = [file for file in pdf_list if get_file_extension(file) == 'pdf']
    print('Quantidade de Arquivos no Diretório: ' + str(files_located))
    print('Quantidade de PDFs no Diretório: ' + str(len(pdfs_located)))
    print('-' * 40, '\n')

    inserted_files = 0
    for pdf in pdfs_located:
        inscricao = get_file_name(pdf)
        file_path = path_pdfs + pdf
        with open(file_path, 'rb') as pdf_content:
            # bindata = pyodbc.Binary(pdf_content.read())
            bindata = pdf_content.read()

            print(f'Inserindo Inscrição: {inscricao}')
            nome_arquivo = pdf.split('_')[0] + '.pdf'
            success = insert_database_row(inscricao=inscricao, nome_arquivo=nome_arquivo, tipo_conteudo=8,
                                          conteudo_binario=bindata, compactado=0)
            if success:
                inserted_files += 1
                print(f'Arquivos inseridos: {inserted_files} de {pdfs_located}\n', )


if __name__ == '__main__':
    insert_pdfs()
