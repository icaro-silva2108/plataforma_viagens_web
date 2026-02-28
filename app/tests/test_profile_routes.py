from app.database.connection import get_connection
import uuid
from unittest.mock import patch

# Teste da rota protegida profile com método Get
def test_get_profile_route(user_tokens):

    client = user_tokens.get("client")
    access_token = user_tokens.get("access_token")
    response = client.get("/api/profile", headers={"Authorization" : "Bearer {}".format(access_token)})

    assert response is not None
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["user"] is not None
    assert response.json["user"]["id"] is not None

# Testa rota protegida profile com método Get sem o header de autorização
def test_get_profile_authorization_error(client_no_ratelimit):

    client = client_no_ratelimit
    response = client.get("/api/profile", json={
        "name" : "novo nome"
    })

    assert response is not None
    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Header de autorização não encontrado"

# Testa rota profile com método Get sem identidade do token
def test_get_profile_none_identity(user_tokens, mock_none_identity_fixture):

    access_token = user_tokens.get("access_token")

    client = user_tokens.get("client")
    response = client.get("/api/profile", headers={
        "Authorization" : "Bearer {}".format(access_token)
        })

    assert response is not None
    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Usuário não existe ou não está autorizado"

# Testa rota protegida profile com método Patch
def test_patch_profile_route(user_tokens):
    conn = None
    cursor = None
    email = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        email = f"email@{str(uuid.uuid4())}.com"

        client = user_tokens.get("client")
        access_token = user_tokens.get("access_token")
        response = client.patch("/api/profile", json={
            "name" : "novo nome",
            "email" : email,
            "password" : "novasenha",
            "password_confirm" : "novasenha",
            "birth_date" : "2000-08-08"
        },
        headers={
            "Authorization" : "Bearer {}".format(access_token)
        })

        assert response is not None
        assert response.status_code == 200
        assert response.json["success"] is True
        assert response.json["message"] == "Dados alterados com sucesso."

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Testa rota protegida profile com método Patch sem o header de autorização
def test_patch_profile_authorization_error(client_no_ratelimit):

    client = client_no_ratelimit
    response = client.patch("/api/profile", json={
        "name" : "novo nome"
    })

    assert response is not None
    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Header de autorização não encontrado"

def test_patch_profile_none_identity(user_tokens, mock_none_identity_fixture):


    access_token = user_tokens.get("access_token")

    client = user_tokens.get("client")
    response = client.patch("/api/profile", json={
        "name" : "novo nome"
    },
    headers={
        "Authorization" : "Bearer {}".format(access_token)
    })

    assert response is not None
    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Usuário não existe ou não está autorizado"