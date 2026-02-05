from app.database.connection import get_connection
from datetime import datetime, date

def search_user_info(email):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT id, name, password_hash
            FROM users 
            WHERE email = %s;
            """

        cursor.execute(sql, (email,))
        user_info = cursor.fetchone()

        return user_info# --> Retorna as informações do usuário, ou None se não existir.

    except Exception:
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_user_by_id(user_id):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT name, email, birth_date
            FROM users
            WHERE id = %s;
            """

        cursor.execute(sql, (user_id, ))
        user = cursor.fetchone()

        return user

    except Exception:
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_destination(destination_id):# --> Procura o id do destino para fazer verificações de existência e retorna o id verificado

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT id FROM destinations WHERE id = %s AND active = TRUE"# --> Verifica se o id existe no banco e se está ativo
        cursor.execute(sql, (destination_id, ))
        id_row = cursor.fetchone()

        if id_row:
            return id_row[0]# --> Se existir, retorna o id da reserva verificado
        else:
            return None# --> Se não houver, indica que não encontrou

    except Exception:
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def birth_date_validation(birth_date_str):

    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    today = date.today()
    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    if age < 16:
        return None

    return birth_date

def travel_date_validation(travel_date_str):

    try:
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    if travel_date <= date.today():
        return None

    return travel_date