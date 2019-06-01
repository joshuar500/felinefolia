import stripe
import os

from flask import Flask
from flask_cors import CORS
from celery import Celery

from felinefolia.resources import views
from felinefolia.extensions import (
    mail,
    db,
    jwt
)

from lib.util_decorators import add_user_claims_loader

CELERY_TASK_LIST = [
    'felinefolia.resources.user.tasks',
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(testing=False, settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    # TODO: check if production or development server
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    # Load production environment settings
    if os.environ.get('PRODUCTION'):
        app.config.from_pyfile('prod_settings.py')

    # Load end to end testing settings
    if testing is True:
        app.config.from_object('config.test_settings')
        app.config.from_pyfile('test_settings.py', silent=True)

    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    stripe.api_version = app.config.get('STRIPE_API_VERSION')

    extensions(app)

    add_user_claims_loader(jwt)

    app.register_blueprint(views.blueprint)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    return None
