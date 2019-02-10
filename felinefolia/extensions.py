from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()