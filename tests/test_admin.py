import factory
from pytest_factoryboy import register
from flask_jwt_extended import (
    create_access_token
)

from felinefolia.resources.user.models import User

from flask_jwt_extended import create_access_token


@register
class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@mail.com' % n)
    password = 'mypwd'

    class Meta:
        model = User


def test_get_users(app, client, db, admin_json_access_token):
    # returns all users
    rep = client.get('/api/v1/users', json=admin_json_access_token)
    assert rep.status_code == 200

    # no access token
    rep = client.get('/api/v1/users')
    assert rep == 401
