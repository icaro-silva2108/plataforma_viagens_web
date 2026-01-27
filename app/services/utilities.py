from app.database.connection import get_connection

def search_user_by_email(email):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        email_query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)"
        cursor.execute(email_query, (email,))
        email_result = bool(cursor.fetchone()[0])# --> Garante que exista um usuário a ser buscado

        if email_result:

            id_query = "SELECT id FROM users WHERE email = %s;"
            cursor.execute(id_query, (email,))
            user_id = cursor.fetchone()[0]

            return user_id# --> Retorna o id do usuário buscado pelo email

        else:
            return None# --> Se não encontrar, retorna None

    except Exception as e:
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_password_hash(email):# --> Encontra o hash da senha do usuário através do email para fazer verificação no login em user_service

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        user_id = search_user_by_email(email)# --> Verifica se o usuário existe
        if user_id:

            sql = "SELECT password_hash FROM users WHERE email = %s"
            cursor.execute(sql, (email, ))
            pw_hash = cursor.fetchone()[0]# --> Se existir, busca pela hash de senha dele

            return pw_hash

        else:
            return None# --> Se não achar, retorna None e barra o login se a senha estiver errada

    except Exception as e:
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_name_user(user_id):# --> Retorna o nome do usuário a partir do seu id

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if user_id:# --> Confere se o usuário existe

            sql = "SELECT name FROM users WHERE id = %s"
            cursor.execute(sql, (user_id, ))
            name = cursor.fetchone()[0]

            return name# --> Se encontrar, retorna o nome buscado no database.

        else:
            return None# --> Caso, contrário, retorna None

    except Exception as e:
        raise e

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

        sql = "SELECT id FROM destinations WHERE id = %s AND active = 1"# --> Verifica se o id existe no banco e se está ativo
        cursor.execute(sql, (destination_id, ))
        id_row = cursor.fetchone()

        if id_row:
            return id_row[0]# --> Se existir, retorna o id da reserva verificado
        else:
            return None# --> Se não houver, indica que não encontrou

    except Exception as e:
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()