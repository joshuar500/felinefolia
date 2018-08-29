import secrets
import string

from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    url_for,
    make_response,
    render_template)
from flask_restful import Api, Resource, url_for, reqparse, fields, marshal_with
from flask_jwt_extended import (
  jwt_required,
  get_jwt_identity,
  create_access_token,
  create_refresh_token,
  set_access_cookies,
  set_refresh_cookies,
  get_csrf_token
)

from felinefolia.blueprints.user.models import User
from felinefolia.blueprints.contact.models import Comment

user = Blueprint('user', __name__)
api = Api(user)

def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    # if valid_email(email_str):
    #     return email_str
    # else:
    #     raise ValueError('{} is not a valid email'.format(email_str))
    return email_str

register_parser = reqparse.RequestParser()
register_parser.add_argument(
    'username', dest='username',
    required=True,
    help='The user\'s username',
)
register_parser.add_argument(
    'email', dest='email',
    type=email,
    required=True, help='The user\'s email',
)
register_parser.add_argument(
    'password', dest='password',
    required=True, help='The user\'s password',
)
register_parser.add_argument(
    'user_priority', dest='user_priority',
    type=int,
    default=1, choices=range(5), help='The user\'s priority',
)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'user_priority': fields.Integer,
    'custom_greeting': fields.FormattedString('Hey there!'),
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime
}

class Register(Resource):

  @marshal_with(user_fields)
  def post(self):
    args = register_parser.parse_args()
    user = User(username=args.username)
    user.password = user.encrypt_password(args.password)
    user.save()
    return user, 200

pre_register_parser = reqparse.RequestParser()
pre_register_parser.add_argument('email', required=True, type=email)
pre_register_parser.add_argument('optional')
pre_register_parser.add_argument('hasBusiness', type=bool)

class PreRegister(Resource):
  def post(self):
    args = pre_register_parser.parse_args()
    email = args.email
    optional = args.optional
    has_business = args.hasBusiness

    found_user = User.find_by_identity(args.email)
    if not found_user:
      user = User(username=email, email=email, has_business=has_business)

      # generate a password for user
      alphabet = string.ascii_letters + string.digits
      password = ''.join(secrets.choice(alphabet) for i in range(20))

      user.password = user.encrypt_password(password)
      user.save()

      comment = Comment()
      comment.user_id = user.id
      comment.comment = optional
      comment.save()
      return { 'message': 'Account created.' }, 200
    return { 'message': 'User already exists.' }, 500

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True)
login_parser.add_argument('password', required=True)

class Login(Resource):

  def post(self):
    # TODO: Parse arguments like Register
    args = login_parser.parse_args()
    user = User.find_by_identity(args.username)
    if user and user.authenticated(password=args.password):

      current_user = {
        'username': user.username,
        'role': user.role,
        'email': user.email
      }

      access_token = create_access_token(identity=current_user)
      refresh_token = create_refresh_token(identity=current_user)

      # obj = {
      #   'message': 'yay you logged in',
      #   'access_csrf': get_csrf_token(access_token),
      #   'refresh_csrf': get_csrf_token(refresh_token)
      #   }

      resp = make_response()

      set_access_cookies(resp, access_token)
      set_refresh_cookies(resp, refresh_token)

      return resp
    return { "Error": "Something went wrong." }, 401

class Account(Resource):

  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    print(current_user)
    return current_user, 200

api.add_resource(Register, '/register')
api.add_resource(PreRegister, '/preregister')
api.add_resource(Login, '/login')
api.add_resource(Account, '/account')
