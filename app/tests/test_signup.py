from main import app
from app.database.connection import get_connection
import uuid

# Testa login com um email aleatório
def test_signup_success_login():

    conn = None
    cursor = None
    response = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        email_id = str(uuid.uuid4())
        email = f"teste@{email_id}.com"

        client = app.test_client()
        response = client.post("/api/signup", json={
            "name" : "teste",
            "email" : email,
            "password" : "teste123",
            "password_confirm" : "teste123",
            "birth_date" : "2000-01-01"
        })

    finally:
        if cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (email, ))
            conn.commit()
            cursor.close()
        if conn:
            conn.close()

    assert response is not None
    assert response.status_code == 201
    assert response.json["success"] is True

# Testa JSON inválido
def test_signup_not_valid_json():

    client = app.test_client()
    response = client.post("/api/signup", json={})

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "JSON inválido"

# Testa JSON com campos vazios
def test_signup_empty_fields():

    client = app.test_client()
    response = client.post("/api/signup", json={
        "name" : "",
        "email" : "",
        "password" : "",
        "password_confirm" : "",
        "birth_date" : ""
    })

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "Campos vazios. Preencha todos os campos."

# Testa email com formato inválido
def test_signup_invalid_email_format():

    client = app.test_client()
    response = client.post("/api/signup", json={
        "name" : "teste",
        "email" : "teste.teste",
        "password" : "teste123",
        "password_confirm" : "teste123",
        "birth_date" : "2000-01-01" 
    })

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "Formato de email inválido(email@email.com)."

# Testa cadastro com email já existente
def test_signup_email_already_taken():

    conn = None
    cursor = None
    first_user_response = None
    second_user_response = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        email_id = str(uuid.uuid4())
        email = f"teste@{email_id}.com"

        client = app.test_client()
        first_user_response = client.post("/api/signup", json={
            "name" : "teste",
            "email" : email,
            "password" : "teste123",
            "password_confirm" : "teste123",
            "birth_date" : "2000-01-01"
        })

        second_user_response = client.post("/api/signup", json={
            "name" : "teste",
            "email" : email,
            "password" : "teste123",
            "password_confirm" : "teste123",
            "birth_date" : "2000-01-01"
        })

    finally:
        if cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (email, ))
            conn.commit()
            cursor.close()
        if conn:
            conn.close()

    assert first_user_response is not None
    assert second_user_response is not None
    assert first_user_response.status_code == 201
    assert first_user_response.json["success"] is True
    assert second_user_response.status_code == 409
    assert second_user_response.json["success"] is False
    assert second_user_response.json["message"] == "Este email já está sendo utilizado. Tente outro email."

# Testa confirmação da senha diferente da senha
def test_signup_invalid_password_confirm():

    client = app.test_client()
    response = client.post("/api/signup", json={
        "name" : "teste",
        "email" : "teste@teste.com",
        "password" : "teste123",
        "password_confirm" : "teste",
        "birth_date" : "2000-01-01"
    })

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "A senha e sua confirmação devem ser iguais."

# Testa formato de data inválido
def test_signup_invalid_birth_date_format():

    client = app.test_client()
    response = client.post("/api/signup", json={
        "name" : "teste",
        "email" : "teste@teste.com",
        "password" : "teste123",
        "password_confirm" : "teste123",
        "birth_date" : "01-01-2000"
    })

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "Formato de data inválido (dd/mm/aaaa)."

# Testa idade maior de 16 anos
def test_signup_invalid_birth_date_age():

    client = app.test_client()
    response = client.post("/api/signup", json={
        "name" : "teste",
        "email" : "teste@teste.com",
        "password" : "teste123",
        "password_confirm" : "teste123",
        "birth_date" : "2026-02-20"
    })

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "É preciso ter pelo menos 16 anos pra criar uma conta."