import pandas as pd
import pyodbc


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


def log_erro(inscricao):
    with open('log_update.txt', 'a') as file:
        file.write(inscricao + '\n')


def update_database_row(inscricao, nome_arquivo, tipo_conteudo, conteudo_binario):
    params = (
        inscricao,  # existing COD_CONTEUDO_BINARIO
        conteudo_binario,  # CONTEUDO_BINARIO
        nome_arquivo,  # NOME_ARQUIVO
        tipo_conteudo,  # TIPO_CONTEUDO_BINARIO
        inscricao,  # COD_CONTEUDO_BINARIO
    )

    connection = get_connection()
    cursor = get_cursor(connection)

    success = False
    try:
        cursor.execute('''
            BEGIN 
                IF EXISTS (
                    SELECT COD_CONTEUDO_BINARIO FROM [dbo].[FW_CONTEUDOS_BINARIOS]
                    WHERE COD_CONTEUDO_BINARIO = ?
                )
                BEGIN
                UPDATE [dbo].[FW_CONTEUDOS_BINARIOS]
                SET CONTEUDO_BINARIO = ?,
                    NOME_ARQUIVO = ?
                WHERE TIPO_CONTEUDO_BINARIO = ?
                    AND COD_CONTEUDO_BINARIO = ?
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


def update_pdfs(planilha, diretorio_pdfs):
    df = pd.read_excel(planilha, index_col=None, header=None)

    inscricoes = df[2]
    codigos = df[3]

    for count, i in enumerate(range(len(df))):
        if count > 0:
            inscricao = int(inscricoes[i])
            codigo = str(codigos[i])

            with open(diretorio_pdfs + codigo + '_1.pdf', 'rb') as pdf_content:
                bindata = pyodbc.Binary(pdf_content.read())
                # bindata = pdf_content.read()

                print(f'Atualizando Inscrição: {inscricao}')
                nome_arquivo = str(inscricao) + '.pdf'
                success = update_database_row(inscricao=inscricao, nome_arquivo=nome_arquivo, tipo_conteudo=8,
                                              conteudo_binario=bindata)
                if success:
                    print(f'Arquivos atualizados: {count}')


if __name__ == '__main__':
    planilha = 'C:\\Users\\2019201410840742\\Documents\\project\\candidatos2.xlsx'
    diretorio_pdfs = 'C:\\Users\\2019201410840742\\Documents\\project\\pdfs\\'
    update_pdfs(planilha=planilha, diretorio_pdfs=diretorio_pdfs)
