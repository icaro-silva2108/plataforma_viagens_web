from app.database.connection import get_connection
from app.services.utilities import search_user_by_email

"""
Variáveis 'conn'(conexão ao banco) e 'cursor'(meio entre python e banco) recebendo None servem de garantia para que elas existam e não quebrem o código.
A variável 'sql' é um código sql a ser executado pelo comando cursor.execute(...).
A variável 'sql' possui Placeholders(%s) contra sql injection.
conn.comit() acompanha o cursor.execute() para salvar as alterações feitas no database.
Blocos finally servem para garantir que a conexão e o cursor serão interrompidos, impedindo acesso desnecessário ao banco e consumo de memória.
Blocos except tratam o retorno do database a um estado estável com rollback e apresenta o erro ocorrido.
O bloco cursor.rowcount é para fins de verificação de alterações no banco. Se houve alteração salva com commit, se não houve retorna ao estado anterior.
"""

def create_reservation(user_id, destination_id, travel_date):# --> Cria nova reserva

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO reservations (user_id, destination_id, travel_date) VALUES (%s, %s, %s)"

        cursor.execute(sql, (user_id, destination_id, travel_date))

        conn.commit()
        return True# --> Confirma que a reserva foi criada

    except Exception as e:
        if conn:
            conn.rollback()
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def cancel_reservation(reservation_id, user_id):# --> Cancela uma reserva por referência de email(por ser único para cada usuário) e id da reserva especificando qual será cancelada

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM reservations WHERE id = %s AND user_id = %s"# --> Identifica o id do usuário pelo email através de uma subquery

        cursor.execute(sql, (reservation_id, user_id))

        if cursor.rowcount > 0:
            conn.commit()
            return True# --> Confirma que a reserva foi cancelada
        else:
            conn.rollback()
            return False# --> A reserva não existia ou não pertencia ao usuário

    except Exception as e:
        if conn:
            conn.rollback()
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def show_reservations(user_id):# --> Mostra as reservas feitas pelo usuário através de seu id

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

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
        return results# --> Retorna as reservas buscadas pelo id do usuário

    except Exception as e:
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
