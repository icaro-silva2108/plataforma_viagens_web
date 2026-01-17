from app.database.connection import get_connection

"""
Variáveis 'conn'(conexão ao banco) e 'cursor'(meio entre python e banco) recebendo None servem de garantia para que elas existam e não quebrem o código.
A variável 'sql' é um código sql a ser executado pelo comando cursor.execute(...)
A variável 'sql' possui Placeholders(%s) contra sql injection
conn.comit() acompanha o cursor.execute() para salvar as alterações feitas no database
Blocos finally servem para garantir que a conexão e o cursor serão interrompidos, impedindo acesso desnecessário ao banco e consumo de memória.
Blocos except tratam o retorno do database a um estado estável com rollback e apresenta o erro ocorrido
"""

def create_user(name, email, password_hash, birth_date):# --> Criação de novo usuário
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO users (name, email, password_hash, birth_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, email, password_hash, birth_date))

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

def delete_user(email):# --> Exclui o cadastro do usuário

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        id_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(id_query, (email,))
        user_id = cursor.fetchone()[0]

        rows_select = ("SELECT COUNT(*) FROM reservations WHERE user_id = %s")
        cursor.execute(rows_select, (user_id,))
        rows = cursor.fetchone()[0]#--> Verifica se o usuário tem reservas

        if rows < 1:    

            sql = ("DELETE FROM users WHERE id = %s")# --> Se não tiver reservas, pode ter o cadastro excluído

            cursor.execute(sql, (user_id,))
            
            conn.commit()
            return True

        else:# --> Se tiver reservas, deverá cancelar primeiro antes de excluir o cadastro
            return False

    except Exception as e:
        if conn:
            conn.rollback()
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()