import pytest
from src.auth.models import User

# from src.logger import logger
from sqlalchemy import select, text


# === API LEVEL TESTS ===
def test_create_user(client):
    """Test that `/api/user/get-users correctly functions on valid inputs and exists in the DB by calling the user `GET` functions"""
    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        "/api/user/create-user",
        json={
            "email": "test@example.com",
            "first_name": "first test name",
            "last_name": "last test name",
            "password": "somepassword",
        },
    )
    assert response.status_code == 200

    response = client.get(f"/api/user/get-user?id={response.json().get('id')}")
    assert response.status_code == 200
    assert response.json() == {
        "id": response.json().get("id"),
        "email": "test@example.com",
        "first_name": "first test name",
        "last_name": "last test name",
    }

    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_duplicate_emails_signup(client):
    """Tests that when a user fails to signup with an existing email, they receive HTTP 409 and that the `GET` functions correctly show that the user does not exist"""
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


# === DB LEVEL TESTS ===
async def test_duplicate_email_is_atomic(client, db_session):
    """Tests that when a duplicate email is submitted, return HTTP 409 and a second user row is not inserted"""
    payload = {
        "email": "alaturing@gmail.com",
        "first_name": "alan",
        "last_name": "turing",
        "password": "computerscool",
    }

    resp1 = client.post("/api/user/create-user", json=payload)
    assert resp1.status_code == 200

    user_id = resp1.json().get("id")
    assert user_id is not None

    resp2 = client.post("/api/user/create-user", json=payload)
    assert resp2.status_code == 409

    # verify DB level
    result = await db_session.execute(
        select(User).where(User.email == payload["email"])
    )
    users = result.scalars().all()
    assert len(users) == 1
    assert users[0].id == user_id


async def test_connect_rolls_back_on_error(db_session):
    """Tests that upon error, a DB transaction rolls back and is not commited"""
    from src.sockets.utils import generate_short_id

    id = generate_short_id()

    with pytest.raises(RuntimeError):
        async with db_session.begin():
            await db_session.execute(
                text("""
                    INSERT INTO users (id, email, password, first_name, last_name)
                    VALUES (:id, :email, :password, :first_name, :last_name)
                """),
                {
                    "id": id,
                    "email": "rollback@example.com",
                    "password": "pw",
                    "first_name": "first",
                    "last_name": "last",
                },
            )
            raise RuntimeError("Failure mid transaction")

    result = await db_session.execute(
        select(User).where(User.email == "rollback@example.com")
    )
    users = result.scalars().all()
    assert users == []
