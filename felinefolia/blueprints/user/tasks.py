import redis
from lib.flask_mailplus import send_template_message
from felinefolia.app import create_celery_app
from felinefolia.blueprints.user.models import User
from datetime import timedelta

celery = create_celery_app()
revoked_store = redis.StrictRedis.from_url('redis://:devpassword@redis:6379/0')
ACCESS_EXPIRES = timedelta(minutes=15)

@celery.task()
def set_revoked_token(revoked_token, is_revoked):
  revoked_store.set(revoked_token, is_revoked, ACCESS_EXPIRES * 1.2)