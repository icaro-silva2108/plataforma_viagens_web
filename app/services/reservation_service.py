from app.database.connection import get_connection

"""
Variáveis 'conn'(conexão ao banco) e 'cursor'(meio entre python e banco) recebendo None servem de garantia para que elas existam e não quebrem o código.
A variável 'sql' é um código sql a ser executado pelo comando cursor.execute(...)
A variável 'sql' possui Placeholders(%s) contra sql injection
conn.comit() acompanha o cursor.execute() para salvar as alterações feitas no database
Blocos finally servem para garantir que a conexão e o cursor serão interrompidos, impedindo acesso desnecessário ao banco e consumo de memória.
Blocos except tratam o retorno do database a um estado estável com rollback e apresenta o erro ocorrido
"""

def create_reservation(email, destination_id, travel_date):# --> Cria nova reserva

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        id_query = "SELECT id FROM users WHERE email = %s"# --> Query separada para buscar id do usuário através do email
        cursor.execute(id_query, (email,))
        user_id = cursor.fetchone()[0]

        sql = "INSERT INTO reservations (user_id, destination_id, travel_date) VALUES (%s, %s, %s)"

        cursor.execute(sql, (user_id, destination_id, travel_date))# --> user_id referencia o id de usuário em users no database, assim como o destination_id com o id de destino em destinations

        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def cancel_reservation(reservation_id, email):# --> Cancela uma reserva por referência de email(por ser único para cada usuário) e id da reserva especificando qual será cancelada

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM reservations WHERE id = %s AND user_id = (SELECT id FROM users WHERE email = %s)"# --> Identifica o id do usuário pelo email através de uma subquery

        cursor.execute(sql, (reservation_id, email))

        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def show_reservations(email):# --> Mostra as reservas feitas pelo usuário através de seu id

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        id_query = "SELECT id FROM users WHERE email = %s"# --> Query separada para buscar id do usuário através do email
        cursor.execute(id_query, (email,))
        user_id = cursor.fetchone()[0]

        sql ="""SELECT
                r.id, 
                d.city, 
                d.country, 
                r.travel_date, 
                r.status, 
                d.price
                FROM destinations d
                INNER JOIN reservations r ON d.id = r.destination_id
                WHERE r.user_id = %s"""

        cursor.execute(sql, (user_id,))
        results = cursor.fetchall()
        return results

    except Exception as e:
        raise e

    finally:

        if cursor:
            cursor.close()
        if conn:
            conn.close()
