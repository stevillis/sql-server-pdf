import sqlite3


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_BLOB(name, pdf):
    connection = None
    try:
        connection = sqlite3.connect('sqlite3.db')
        cursor = connection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """INSERT INTO test (name, pdf) VALUES (?, ?)"""

        emp_pdf = convert_to_binary_data(pdf)

        # Convert data into tuple format
        data_tuple = (name, emp_pdf)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        connection.commit()
        print("PDF inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("the sqlite connection is closed")


def read_BLOB():
    connection = None
    try:
        connection = sqlite3.connect('sqlite3.db')
        cursor = connection.cursor()

        cursor.execute('SELECT pdf FROM test WHERE id=1;')
        pdf = cursor.fetchone()[0]
        with open('../result.pdf', 'wb') as file:
            file.write(pdf)
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("the pdf was read from table and saved to disk")


# insert_BLOB("Smith", 'C:\\Users\\2019201410840742\\Documents\\dummy.pdf')
# insert_BLOB("David", 'C:\\Users\\2019201410840742\\Documents\\dummy2.pdf')

# Reading file from database
read_BLOB()
