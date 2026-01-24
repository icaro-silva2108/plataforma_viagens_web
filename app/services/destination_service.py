from app.database.connection import get_connection

"""
Variáveis 'conn'(conexão ao banco) e 'cursor'(meio entre python e banco) recebendo None servem de garantia para que elas existam e não quebrem o código.
A variável 'sql' é um código sql a ser executado pelo comando cursor.execute(...).
Blocos except tratam e apresentam o erro ocorrido.
Blocos finally servem para garantir que a conexão e o cursor serão interrompidos, impedindo acesso desnecessário ao banco e consumo de memória.
"""

def show_destinations():

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT city, country, description, price FROM destinations;"
        cursor.execute(sql)
        results = cursor.fetchall()

        return results# --> Retorna os destinos disponíveis buscados no database

    except Exception as e:
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()