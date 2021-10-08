"""

import pyodbc

server = 'tcp:myserver.database.windows.net'
database = 'mydb'
username = 'myusername'
password = 'mypassword'
connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = connection.cursor()


cursor.execute(
    '''
    CREATE TABLE test (
        id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
        nome VARCHAR(200) NOT NULL,
        pdf VARBINARY(max) NOT NULL
    );
    '''
)

connection.commit()
"""

"""
cursor.execute(
    '''
    INSERT INTO test 
    (pdf)
    (SELECT * FROM OPENROWSET(BULK 'C:\\Users\\2019201410840742\\Documents\\dummy.pdf', SINGLE_BLOB) AS BLOB;
    '''
)
"""

file = 'C:\\Users\\2019201410840742\\Documents\\dummy.pdf'
# insert = 'INSERT INTO test (nome, pdf) values (?, ?)'

with open(file, 'rb') as f:
    bindata = f.read()

print(bindata)

# binparams = (file, pyodbc.Binary(bindata))

# connection.cursor().execute(insert, binparams)
# connection.commit()
# connection.close()
