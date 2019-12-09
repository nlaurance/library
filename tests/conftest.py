import json
import pytest

from library.models import User
from library.models import BookRequest
from library.app import create_app
from library.extensions import db as _db


@pytest.fixture
def book_request(db):
    book_request = BookRequest(email="me@myself.com", book_id=1,)
    db.session.add(book_request)
    db.session.commit()
    return book_request


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(username="admin", email="admin@admin.com", password="admin")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user, client):
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["access_token"],
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["refresh_token"],
    }
