from datetime import datetime, timedelta
from freezegun import freeze_time

""" Testes da rota refresh"""

# Testa sucesso ao renovar token
def test_refresh_success(user_tokens):

    client = user_tokens.get("client")
    refresh_token = user_tokens.get("refresh_token")
    access_token_before = user_tokens.get("access_token")

    response = client.post("/api/refresh", headers={"Authorization" : "Bearer {}".format(refresh_token)})

    assert response is not None
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["access_token"] is not None
    assert response.json["access_token"] != access_token_before

# Testa rota com erro
def test_refresh_error(user_tokens, mock_exception_send_access_token):

    client = user_tokens.get("client")
    refresh_token = user_tokens.get("refresh_token")

    response = client.post("/api/refresh", headers={"Authorization" : "Bearer {}".format(refresh_token)})

    assert response is not None
    assert response.status_code == 500
    assert response.json["success"] is False
    assert response.json["message"] == "Erro interno: Erro simulado"

# Testa rota com token inválido
def test_refresh_invalid_token_type(user_tokens):

    client = user_tokens.get("client")
    access_token = user_tokens.get("access_token")

    response = client.post("/api/refresh", headers={"Authorization" : "Bearer {}".format(access_token)})

    assert response is not None
    assert response.status_code == 422
    assert response.json["msg"] == "Only refresh tokens are allowed"

# Testa rota com token expirado
def test_refresh_expired_token(user_tokens):

    client = user_tokens.get("client")
    refresh_token = user_tokens.get("refresh_token")

    expired = datetime.now() + timedelta(days=8)
    with freeze_time(expired):

        response = client.post("/api/refresh", headers={"Authorization" : "Bearer {}".format(refresh_token)})

        assert response is not None
        assert response.status_code == 401

"""Testes rota logout"""

# Testa logout bem sucedido
def test_logout_success(user_tokens):

    client = user_tokens.get("client")
    refresh_token = user_tokens.get("refresh_token")

    response = client.post("/api/logout", headers={"Authorization" : "Bearer {}".format(refresh_token)})

    assert response is not None
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["message"] == "Logout realizado com sucesso. Refresh Token revogado."

# Testa rota com erro
def test_logout_error(user_tokens, mock_exception_add_revoked_tokens):

    client = user_tokens.get("client")
    refresh_token = user_tokens.get("refresh_token")

    response = client.post("/api/logout", headers={"Authorization" : "Bearer {}".format(refresh_token)})

    assert response is not None
    assert response.status_code == 500
    assert response.json["success"] is False
    assert response.json["message"] == "Erro interno: Erro simulado"

# Testa rota com revogação não concluida
def test_none_revoke_confirm(user_tokens, mock_add_revoked_tokens_none):

    client = user_tokens.get("client")
    refresh_token = user_tokens.get("refresh_token")

    response = client.post("/api/logout", headers={"Authorization" : "Bearer {}".format(refresh_token)})

    assert response is not None
    assert response.status_code == 500
    assert response.json["success"] is False
    assert response.json["message"] == "Não foi possível revogar o Refresh Token."

# Testa rota com token inválido
def test_logout_invalid_token_type(user_tokens):

    client = user_tokens.get("client")
    access_token = user_tokens.get("access_token")

    response = client.post("/api/refresh", headers={"Authorization" : "Bearer {}".format(access_token)})

    assert response is not None
    assert response.status_code == 422
    assert response.json["msg"] == "Only refresh tokens are allowed"

# Testa logout com token expirado
def test_logout_expired_token(user_tokens):

    client = user_tokens.get("client")
    refresh_token = user_tokens.get("refresh_token")

    expired = datetime.now() + timedelta(days=8)
    with freeze_time(expired):
        
        response = client.post("/api/logout", headers={"Authorization" : "Bearer {}".format(refresh_token)})

        assert response is not None
        assert response.status_code == 401