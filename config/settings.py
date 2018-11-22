# 
# DEV ENVIRONMENT CONFIG
# FOR PROD CONFIG, ASK ADMIN
# 

from datetime import timedelta

from celery.schedules import crontab


DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = 'felinefolia.local:8000'
SECRET_KEY = 'insecurekeyfordev'

JWT_TOKEN_LOCATION = 'cookies'
JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/token/refresh'
JWT_COOKIE_CSRF_PROTECT = False
JWT_SECRET_KEY = SECRET_KEY

# Flask-Mail.
MAIL_DEFAULT_SENDER = 'contact@local.host'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'you@gmail.com'
MAIL_PASSWORD = 'awesomepassword'

# Flask-Babel.
LANGUAGES = {
    'en': 'English',
    'kr': 'Korean',
    'es': 'Spanish'
}
BABEL_DEFAULT_LOCALE = 'en'

# Celery.
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
# CELERYBEAT_SCHEDULE = {
#     'mark-soon-to-expire-credit-cards': {
#         'task': 'felinefolia.blueprints.billing.tasks.mark_old_credit_cards',
#         'schedule': crontab(hour=0, minute=0)
#     },
#     'expire-old-coupons': {
#         'task': 'felinefolia.blueprints.billing.tasks.expire_old_coupons',
#         'schedule': crontab(hour=0, minute=1)
#     },
# }

# SQLAlchemy.
db_uri = 'postgresql://felinefolia:devpassword@postgres:5432/felinefolia'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)

# Billing.
STRIPE_SECRET_KEY = 'sk_test_nIRds9NsBCaZVRrfy28UD6xX'
STRIPE_PUBLISHABLE_KEY = 'pk_test_8T6wzkJRI6xoB0JgPS9amKS6'
STRIPE_API_VERSION = '2018-09-24'
STRIPE_CURRENCY = 'usd'
STRIPE_PLANS = {
    '0': {
        'id': 'regular',
        'name': 'regular',
        'amount': 100,
        'currency': STRIPE_CURRENCY,
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'FELINEFOLIA REGULAR',
        'metadata': {
            'coins': 110
        }
    }
}

RATELIMIT_STORAGE_URL = CELERY_BROKER_URL
RATELIMIT_STRATEGY = 'fixed-window-elastic-expiry'
RATELIMIT_HEADERS_ENABLED = True
