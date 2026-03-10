from app.database.connection import get_connection
from datetime import datetime, date
import re

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

        return user# --> Retorna informações do usuário de menor vulnerabilidade

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
            return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def birth_date_validation(birth_date_str):# --> Validação de data de nascimento

    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except ValueError:
        return None, "format" # --> Tipo do erro formato

    today = date.today()
    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    if age < 16:
        return None, "age" # --> Tipo do erro idade

    return birth_date, None

def travel_date_validation(travel_date_str):# --> Validação de data de viagem

    try:
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d").date()
    except ValueError:
        return None, "format"# --> Tipo de erro formato

    if travel_date <= date.today():
        return None, "future"# --> Tipo de erro data do passado ou do dia de hoje

    return travel_date, None

def email_format_validation(email):# --> Padronização de email

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"# --> Formato padrão do email

    if not re.match(pattern, email):
        return None

    return email

def search_user_reservation(user_id):# --> Busca se usuário tem reservas

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        reservation_query = """
            SELECT COUNT(*)
            FROM reservations
            WHERE user_id = %s;
            """
        cursor.execute(reservation_query, (user_id, ))
        reservation_rows = cursor.fetchone()[0]

        return reservation_rows > 0

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_revoked_token(refresh_id):

    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        token_query = """
                    SELECT 1
                    FROM token_blacklist
                    WHERE refresh_id = %s;               
                    """
        
        cursor.execute(token_query, (refresh_id, ))
        result = cursor.fetchone()

        return result is not None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_revoked_tokens(refresh_id):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO token_blacklist (refresh_id) VALUES (%s);"

        cursor.execute(sql, (refresh_id, ))
        conn.commit()
        return True

    except Exception:
        if conn:
            conn.rollback()
            raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()