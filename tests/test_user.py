import factory
from pytest_factoryboy import register

from felinefolia.resources.user.models import User


@register
class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@mail.com' % n)
    password = 'mypwd'

    class Meta:
        model = User


def test_get_user(client, db, user, admin_headers):
    # test 404
    rep = client.get('/api/v1/users/100000', headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    rep = client.get('/api/v1/users%d' % user.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()['user']
    assert data['username'] == user.username
    assert data['email'] == user.email
    assert data['active'] == user.active


def test_put_user(client, db, user, admin_headers):
    # test 404
    rep = client.put("/api/v1/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {'username': 'updated'}

    # test update user
    rep = client.put(
        '/api/v1/users/%d' % user.id,
        json=data,
        headers=admin_headers
    )
    assert rep.status_code == 200

    data = rep.get_json()['user']
    assert data['username'] == 'updated'
    assert data['email'] == user.email
    assert data['active'] == user.active
