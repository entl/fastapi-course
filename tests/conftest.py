import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.main import app
from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token

# Defining database for testing
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}" \
                          f"@{settings.database_hostname}/{settings.database_name}-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # overrides dependency in the routes
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"email": "hello@gmail.com",
                 "password": "123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # password is not returned in response,
    # so we add it manually to have access in login test
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def test_user_2(client):
    user_data = {"email": "hellosecond@gmail.com",
                 "password": "12345"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # password is not returned in response,
    # so we add it manually to have access in login test
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_posts(test_user, test_user_2, session):
    posts_data = [{
        "title": "1st post",
        "content": "1st content",
        "owner_id": test_user["id"]
    }, {
        "title": "2nd post",
        "content": "2nd content",
        "owner_id": test_user["id"]
    }, {
        "title": "3rd post",
        "content": "3rd content",
        "owner_id": test_user_2["id"]
    }]

    # convert dicts to sqlalchemy model
    posts = list(map(lambda post_data: models.Post(**post_data), posts_data))

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()

    return posts
