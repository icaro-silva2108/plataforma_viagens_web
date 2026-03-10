from app.database.connection import get_connection
import uuid
import pytest

"""
Testes rota profile com método GET
"""

# Testa requisição bem sucedida
def test_get_profile_route(user_tokens):

    client = user_tokens.get("client")
    access_token = user_tokens.get("access_token")
    response = client.get("/api/profile", headers={"Authorization" : "Bearer {}".format(access_token)})

    assert response is not None
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["user"] is not None
    assert response.json["user"]["id"] is not None

# Testa rota sem o header de autorização
def test_get_profile_authorization_error(client_no_ratelimit):

    client = client_no_ratelimit
    response = client.get("/api/profile", json={
        "name" : "novo nome"
    })

    assert response is not None
    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Header de autorização não encontrado"

# Testa rota sem identidade do token
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


"""
Testes rota profile com método PATCH
"""

# Testa requisição bem sucedida
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

# Testa rota sem o header de autorização
def test_patch_profile_authorization_error(client_no_ratelimit):

    client = client_no_ratelimit
    response = client.patch("/api/profile", json={
        "name" : "novo nome"
    })

    assert response is not None
    assert response.status_code == 401
    assert response.json["success"] is False
    assert response.json["message"] == "Header de autorização não encontrado"

# Testa rota sem identidade do token
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

# Testa rota sem JSON válido
def test_patch_profile_invalid_json(user_tokens):

    access_token = user_tokens.get("access_token")

    client = user_tokens.get("client")
    response = client.patch("/api/profile", json={}, headers={"Authorization" : f"Bearer {access_token}"})

    assert response is not None
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "JSON inválido"

# Testa rota com campos de alteração vazios
def test_patch_profile_empty_fields(user_tokens):

    access_token = user_tokens.get("access_token")
    client = user_tokens.get("client")

    # Cria loop que faz um request separadamente para cada tipo de dado com campo vazio
    data_types = ["name", "email", "password", "birth_date"]
    for data in data_types:

        if data != "password":
            response = client.patch("/api/profile", json={
                data : ""
            },
            headers={
                "Authorization" : "Bearer {}".format(access_token)
            })

        else:
            response = client.patch("/api/profile", json={
                    data : "",
                    "password_confirm" : ""
                },
                headers={
                    "Authorization" : "Bearer {}".format(access_token)
                })

        assert response is not None
        assert response.status_code == 400
        assert response.json["success"] is False
        assert response.json["message"] == "Não há dados válidos para alterar."

# Testa tratamento de dados da rota
def test_patch_profile_data_treatment(user_tokens):

    access_token = user_tokens.get("access_token")
    client = user_tokens.get("client")

    # Testa o tratamento de formato de email
    email_response = client.patch("/api/profile", json={
        "email" : "emailteste.com"
    },
    headers={
        "Authorization" : "Bearer {}".format(access_token)
    })

    # Testa o tratamento de senha sem confirmação
    no_confirmed_password_response = client.patch("/api/profile", json={
        "password" : "suasenha123",
        "password_confirm" : ""
    },
    headers={
        "Authorization" : "Bearer {}".format(access_token)
    })

    # Testa senha diferete da confirmação
    invalid_password_confirm_response = client.patch("/api/profile", json={
        "password" : "suasenha123",
        "password_confirm" : "suasenha321"
    },
    headers={
        "Authorization" : "Bearer {}".format(access_token)
    })

    # Testa senha com tamanho menor que o mínimo
    invalid_password_lenght_response = client.patch("/api/profile", json={
        "password" : "senha",
        "password_confirm" : "senha"
    },
    headers={
        "Authorization" : "Bearer {}".format(access_token)
    })

    # Testa erro de formato de data de nascimento inválido
    invalid_birth_date_format_response = client.patch("/api/profile", json={
        "birth_date" : "30-12-2000"
    },
    headers={
        "Authorization" : "Bearer {}".format(access_token)
    })

    # Testa erro de idade menor de 16 anos
    invalid_age_response = client.patch("/api/profile", json={
        "birth_date" : "2026-03-10"
    },
    headers={
        "Authorization" : "Bearer {}".format(access_token)
    })

    responses = [
        email_response,
        no_confirmed_password_response,
        invalid_password_confirm_response,
        invalid_password_lenght_response,
        invalid_birth_date_format_response,
        invalid_age_response
        ]
    
    for response in responses:

        assert response is not None
        assert response.status_code == 400
        assert response.json["success"] is False
    
    assert email_response.json["message"] == "Formato de email inválido(email@email.com)."
    assert no_confirmed_password_response.json["message"] == "É necessário fazer a confirmação de senha."
    assert invalid_password_confirm_response.json["message"] == "A senha e a confirmação devem ser iguais."
    assert invalid_password_lenght_response.json["message"] == "A senha precisa ter pelo menos 8 dígitos."
    assert invalid_birth_date_format_response.json["message"] == "Formato de data inválido (dd/mm/aaaa)."
    assert invalid_age_response.json["message"] == "A data a ser alterada deve representar pelo menos 16 anos."