from app.database.connection import get_connection
import uuid

# Testa login com email aleatório
def test_signin_success_login(client_no_ratelimit):

    conn = None
    cursor = None
    response_signup = None
    response_signin = None
    email = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        email = f"teste@{str(uuid.uuid4())}.com"

        client = client_no_ratelimit
        response_signup = client.post("/api/signup", json={
            "name" : "teste",
            "email" : email,
            "password" : "teste123",
            "password_confirm": "teste123",
            "birth_date" : "2000-01-01"
        })

        response_signin = client.post("/api/signin", json={
            "email" : email,
            "password" : "teste123"
        })


    finally:
        if cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (email, ))
            conn.commit()
            cursor.close()

        if conn:
            conn.close()

    assert response_signup is not None
    assert response_signin is not None
    assert response_signup.status_code == 201
    assert response_signup.json["success"] is True
    assert response_signin.status_code == 200
    assert response_signin.json["success"] is True
    assert "access_token" in response_signin.json and "refresh_token" in response_signin.json

# Testa JSON inválido
def test_signin_not_valid_json(client_no_ratelimit):

    client = client_no_ratelimit
    response = client.post("/api/signin", json={})

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "JSON inválido"

# Testa JSON com campos vazios
def test_signin_empty_fields(client_no_ratelimit):

    client = client_no_ratelimit
    response = client.post("/api/signin", json={
        "email": "",
        "password": ""
    })

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "Campos vazios. Preencha todos os campos."

# Testa erro de autenticação
def test_signin_auth_error(client_no_ratelimit):

    client = client_no_ratelimit
    response = client.post("/api/signin", json={
        "email" : "teste@teste.com",
        "password" : "teste123"
    })

    assert response is not None
    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Email ou senha inválidos."