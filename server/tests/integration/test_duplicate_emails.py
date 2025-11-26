def test_duplicate_emails(client):
    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        "/api/user/create-user",
        json={
            "email": "alanturing@gmail.com",
            "first_name": "alan",
            "last_name": "turing",
            "password": "computersrock",
        },
    )
    assert response.status_code == 200

    response = client.get(f"/api/user/get-user?id={response.json().get('id')}")
    assert response.status_code == 200
    assert response.json() == {
        "id": response.json().get("id"),
        "email": "alanturing@gmail.com",
        "first_name": "alan",
        "last_name": "turing",
    }

    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.post(
        "/api/user/create-user",
        json={
            "email": "alanturing@gmail.com",
            "first_name": "primeagen",
            "last_name": "twitch",
            "password": "chussy",
        },
    )

    assert response.status_code == 409

    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 1
