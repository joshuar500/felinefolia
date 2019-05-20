import redis
import requests
import json
from lib.flask_mailplus import send_template_message
from felinefolia.app import create_celery_app
from felinefolia.blueprints.user.models import User
from datetime import timedelta

celery = create_celery_app()
revoked_store = redis.StrictRedis.from_url('redis://:devpassword@redis:6379/0')

ACCESS_EXPIRES = timedelta(minutes=15)

MAILERLITE_API_URL = 'http://api.mailerlite.com/api/v2/'
MAILERLITE_API_KEY = 'ca33ab98e21907bd0616b083ab5b4679'


@celery.task()
def set_revoked_token(revoked_token, is_revoked):
    revoked_store.set(revoked_token, is_revoked, ACCESS_EXPIRES * 1.2)


@celery.task()
def add_subscriber(email):
    url = MAILERLITE_API_URL + 'subscribers'
    data = {
        'email': email,
        'fields': {'purchased_subscription': 0}
    }
    payload = json.dumps(data)
    headers = {
        'content-type': 'application/json',
        'x-mailerlite-apikey': MAILERLITE_API_KEY
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return None


@celery.task()
def deliver_welcome_email(email):
    """
    Send a welcome e-mail.

    :param email: E-mail address of new user
    """

    ctx = {'email': email}

    return None
