import json
import pytest

from felinefolia.resources.user.models import User
from felinefolia.app import create_app
from felinefolia.extensions import db as _db
from felinefolia.resources.auth.helpers import make_auth_response

from flask_jwt_extended import (
    JWTManager,
    create_access_token
)

from lib.util_decorators import add_user_claims_loader

from .helpers.email_generator import generate_random_email


@pytest.fixture
def app():
    app = create_app(testing=True)
    app.config['JWT_SECRET_KEY'] = 'foobarbaz'
    jwt = JWTManager(app)

    add_user_claims_loader(jwt)

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
    random_email = generate_random_email(5)
    user = User(username=random_email, email=random_email,
                password="testdevpassword", role="admin")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def member_user(db):
    random_email = generate_random_email(10)
    user = User(username=random_email, email=random_email,
                password="testdevpassword", role="member")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_json_access_token(app, client):

    access_token = create_access_token({'username': 'testadmin',
                                        'role': 'admin'})

    return {
        'access_token': access_token
    }


@pytest.fixture
def member_json_access_token(app, client, member_user):

    access_token = create_access_token({'username': member_user.username,
                                        'role': member_user.role})

    return {
        'access_token': access_token
    }
