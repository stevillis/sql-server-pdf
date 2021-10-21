import pyodbc
import requests

SERVER = '10.0.0.50'
DATABASE = 'QSELECAO'
USERNAME = 'stevillis'
PASSWORD = '123456@@'


def download_pdf(url):
    response = requests.get(url)
    print(pyodbc.Binary(response.content))


def insert_row():
    connection = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + SERVER + ';DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD)
    cursor = connection.cursor()

    params = (
        1,  # cod_conteudo
        1,  # tipo_conteudo
        'teste1',  # nome_arquivo
        'to aqui',  # conteudo_binario
        1,  # compactado
    )

    cursor.execute(
        '''
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
        END
    ''',
        params
    )

    connection.commit()
    connection.close()


download_pdf('http://www.africau.edu/images/default/sample.pdf')

"""
cursor.execute(
    '''
    INSERT INTO test 
    (pdf)
    (SELECT * FROM OPENROWSET(BULK 'C:\\Users\\2019201410840742\\Documents\\dummy.pdf', SINGLE_BLOB) AS BLOB;
    '''
)
"""

# file = 'C:\\Users\\2019201410840742\\Documents\\dummy.pdf'
# insert = 'INSERT INTO test (nome, pdf) values (?, ?)'

# with open(file, 'rb') as f:
#    bindata = f.read()

# print(bindata)

# binparams = (file, pyodbc.Binary(bindata))

# CONNECTION.cursor().execute(insert, binparams)
# CONNECTION.commit()
# CONNECTION.close()
