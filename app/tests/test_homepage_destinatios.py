from main import app

def test_show_destinations():

    client = app.test_client()
    response = client.get("/api/destinations")

    assert response is not None
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "destinations" in response.json