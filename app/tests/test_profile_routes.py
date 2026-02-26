# Teste da rota protegida profile com método Get
def test_protected_myprofile_route(user_tokens):

    client = user_tokens.get("client")
    access_token = user_tokens.get("access_token")
    response = client.get("/api/profile", headers={"Authorization" : "Bearer {}".format(access_token)})

    assert response is not None
    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["user"] is not None
    assert response.json["user"]["id"] is not None