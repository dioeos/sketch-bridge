import pytest
from src.auth.models import User as UserModel

# from src.logger import logger
from sqlalchemy import select, text


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


async def test_duplicate_emails_verified_signup(client, db_session):
    """Tests that when a user signs up with verified existing email, they receive HTTP 409 and that `GET` only shows 1 row in the user table"""
    await _insert_verified_user(db_session)

    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.post(
        "/api/user/create-user",
        json={
            "email": "verified@example.com",
            "first_name": "first",
            "last_name": "last",
            "password": "password",
        },
    )

    assert response.status_code == 409
    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_duplicate_emails_unverified_signup_updates_kwargs_fields(
    client, db_session
):
    """Tests that when a user signs up with unverified existing email, it updates kwargs fields in DB and user receives HTTP 200"""
    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.post(
        "/api/user/create-user",
        json={
            "email": "email1@example.com",
            "first_name": "first",
            "last_name": "last",
            "password": "password",
        },
    )

    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 1

    result = await db_session.execute(
        select(UserModel).where(UserModel.email == "email1@example.com")
    )
    user = result.scalar_one()
    assert user.is_verified is False
    assert user.first_name == "first"
    assert user.last_name == "last"

    hashed_pass = user.password

    response = client.post(
        "/api/user/create-user",
        json={
            "email": "email1@example.com",
            "first_name": "HELLO",
            "last_name": "WORLD",
            "password": "PYTHON",
        },
    )
    await db_session.refresh(user)

    assert user.is_verified is False

    assert user.first_name == "HELLO"
    assert user.last_name == "WORLD"
    assert user.password != hashed_pass


async def test_duplicate_emails_verified_signup_does_not_update_kwargs_fields(
    client, db_session
):
    """Tests that when a user signs up with verified existing email, it does not update kwargs fields in DB and user receives HTTP 409"""
    await _insert_verified_user(db_session)

    result = await db_session.execute(
        select(UserModel).where(UserModel.email == "verified@example.com")
    )
    user = result.scalar_one()
    assert user.is_verified is True
    assert user.first_name == "first"
    assert user.last_name == "last"
    assert user.password == "pw"

    response = client.post(
        "/api/user/create-user",
        json={
            "email": "verified@example.com",
            "first_name": "notfirst",
            "last_name": "notlast",
            "password": "somepass",
        },
    )

    assert response.status_code == 409

    result = await db_session.execute(
        select(UserModel).where(UserModel.email == "verified@example.com")
    )

    assert user.is_verified is True
    assert user.first_name == "first"
    assert user.last_name == "last"
    assert user.password == "pw"


async def test_duplicate_emails_unverified_signup(client, db_session):
    """Tests that when a user signs up with unverified existing email, they receive HTTP 200 and that `GET` only shows 1 row in the user table"""

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

    # check verification
    result = await db_session.execute(
        select(UserModel).where(UserModel.email == "alanturing@gmail.com")
    )
    user = result.scalar_one()
    assert user.is_verified is False

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

    assert response.status_code == 200

    response = client.get("/api/user/get-users")
    assert response.status_code == 200
    assert len(response.json()) == 1

    result = await db_session.execute(
        select(UserModel).where(UserModel.email == "alanturing@gmail.com")
    )
    user = result.scalar_one()
    assert user.is_verified is False


async def test_duplicate_email_is_atomic(client, db_session):
    """Tests that when a unverified duplicate email is submitted, return HTTP 200 and a second user row is not inserted"""
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
    assert resp2.status_code == 200

    # verify DB level
    result = await db_session.execute(
        select(UserModel).where(UserModel.email == payload["email"])
    )
    users = result.scalars().all()
    assert len(users) == 1
    assert users[0].id == user_id


async def test_connect_rolls_back_on_error(db_session):
    """Tests that upon error, a DB transaction rolls back and is not commited"""

    with pytest.raises(RuntimeError):
        await _insert_and_fail(db_session)

    result = await db_session.execute(
        select(UserModel).where(UserModel.email == "rollback@example.com")
    )
    users = result.scalars().all()
    assert users == []


# ==HELPERS==
async def _insert_and_fail(db_session):
    from src.sockets.utils import generate_short_id

    id = generate_short_id()
    async with db_session.begin():
        await db_session.execute(
            text("""
                INSERT INTO users (id, email, password, first_name, last_name, is_verified)
                VALUES (:id, :email, :password, :first_name, :last_name, :is_verified)
            """),
            {
                "id": id,
                "email": "rollback@example.com",
                "password": "pw",
                "first_name": "first",
                "last_name": "last",
                "is_verified": False,
            },
        )
        raise RuntimeError("Failure mid transaction")


async def _insert_verified_user(db_session):
    from src.sockets.utils import generate_short_id

    id = generate_short_id()
    async with db_session.begin():
        await db_session.execute(
            text("""
                INSERT INTO users (id, email, password, first_name, last_name, is_verified)
                VALUES (:id, :email, :password, :first_name, :last_name, :is_verified)
            """),
            {
                "id": id,
                "email": "verified@example.com",
                "password": "pw",
                "first_name": "first",
                "last_name": "last",
                "is_verified": True,
            },
        )
