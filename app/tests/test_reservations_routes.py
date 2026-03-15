from app.database.connection import get_connection

"""Testes rota reservations com método POST"""

# Testa rota com requisição bem sucedida e com cleanup de registro
def test_create_reservation_success(user_tokens, create_fake_destination):

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        client = user_tokens.get("client")
        access_token = user_tokens.get("access_token")

        create_response = client.post("/api/reservations", json={
            "destination_id" : create_fake_destination.get("fake_destination_id"),
            "travel_date" : "2030-01-01"
        },
        headers={
            "Authorization" : "Bearer {}".format(access_token)
        })

        assert create_response is not None
        assert create_response.status_code == 201
        assert create_response.json["success"] is True
        assert create_response.json["reservation_id"] != None

    finally:
        if cursor:
            cursor.execute("DELETE FROM reservations WHERE id = %s", (create_response.json["reservation_id"], ))

            if conn:
                conn.commit()
                cursor.close()
                conn.close()