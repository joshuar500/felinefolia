import stripe
import os
import redis

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import (
    JWTManager
)
from flask_cors import CORS
from celery import Celery

from felinefolia.blueprints import views

from felinefolia.extensions import (
    mail,
    db,
    jwt
)

CELERY_TASK_LIST = [
    'felinefolia.blueprints.user.tasks',
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


def create_app(settings_override=None):
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

    if os.environ.get('PRODUCTION'):
        print('loading production configuration')
        app.config.from_pyfile('prod_settings.py')

    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    stripe.api_version = app.config.get('STRIPE_API_VERSION')

    extensions(app)

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
