from flask_jwt_extended import (
    create_access_token
)

from felinefolia.resources.user.models import User
from felinefolia.resources.auth.helpers import make_auth_response

from flask_jwt_extended import create_access_token


def test_make_auth_response(app, client, db, monkeypatch):
    app.config['JWT_TOKEN_LOCATION'] = 'cookies'

    def mock_set_revoked_token(token, string):
        return None

    from felinefolia.resources.user import tasks
    monkeypatch.setattr(tasks, 'set_revoked_token', mock_set_revoked_token)

    data = {
        'email': 'testuser@email.com',
        'password': 'testpassword',
        'role': 'member'
    }
    rep = make_auth_response(data)
    assert rep.status_code == 200
    assert rep.headers.has_key('Set-Cookie')


def test_register_user(app, client, db, monkeypatch):

    def mock_add_subscriber(user):
        return None

    from felinefolia.resources.user import tasks
    monkeypatch.setattr(tasks, 'add_subscriber', mock_add_subscriber)

    def mock_make_request(user):
        return user

    from felinefolia.resources.auth import api
    monkeypatch.setattr(api, 'make_auth_response', mock_make_request)

    # register a user
    data = {
        'email': 'testuser@email.com',
        'password': 'testpassword',
        'role': 'member'
    }
    rep = client.post('/api/v1/register', json=data)
    assert rep.status_code == 200

    # TODO: invalid email address
    # data = {
    #     'email': 'testuser',
    #     'password': 'testpassword'
    # }
    # rep = client.post('/api/v1/register')
    # assert rep.status_code == 400
    # assert rep.error.message == 'Invalid email address'
