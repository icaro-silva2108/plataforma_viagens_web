from app.database.connection import get_connection
import uuid

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