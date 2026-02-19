from main import app
from app.database.connection import get_connection
import uuid

# Testa login com um email aleatório
def test_signup():

    conn = None
    cursor = None
    response = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        email_id = str(uuid.uuid4())
        email = f"teste@{email_id}.com"

        # Inicia Client
        client = app.test_client()
        response = client.post("/api/signup", json={
            "name" : "teste",
            "email" : email,
            "password" : "teste123",
            "password_confirm" : "teste123",
            "birth_date" : "2000-01-01"
        })

        if response.status_code == 201:

            sql = """
                DELETE FROM users
                WHERE email = %s
                """

            cursor.execute(sql, (email, ))
            conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    assert response is not None
    assert response.status_code == 201
    assert response.json["success"] is True

# Testa JSON inválido
def test_not_valid_json():

    client = app.test_client()
    response = client.post("/api/signup", json={})

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "JSON inválido"

def test_empty_fields():

    client = app.test_client()
    response = client.post("/api/signup", json={
        "name" : "",
        "email" : "",
        "password" : "",
        "password_confirm" : "",
        "birth_date" : ""
    })

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "Campos vazios. Preencha todos os campos."