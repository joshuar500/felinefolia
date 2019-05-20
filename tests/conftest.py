import pytest

from felinefolia.resources.user.models import User
from felinefolia.app import create_app
from felinefolia.extensions import db as _db


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
    user = User(username='admin', email='admin@admin.com',
                password="admin", role="admin")

    db.session.add(user)
    db.session.commit()

    return user
