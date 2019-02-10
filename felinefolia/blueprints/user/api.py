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
  set_access_cookies,
  set_refresh_cookies,
  get_csrf_token,
  jwt_refresh_token_required,
  get_raw_jwt,
)

from felinefolia.blueprints.user.models import User
from felinefolia.blueprints.user.helpers import make_auth_response
from felinefolia.blueprints.user.parsers import registration_parser, login_parser
from felinefolia.blueprints.contact.models import Comment

user = Blueprint('user', __name__)
api = Api(user)

class Register(Resource):

  def post(self):
    args = registration_parser().parse_args()
    found_user = User.find_by_identity(args.email)
    if not found_user:
      user = User(username=args.email, email=args.email)
      user.password = user.encrypt_password(args.password)
      user.save()

      current_user = {
        'username': user.username,
        'role': user.role,
        'email': user.email
      }

      resp = make_auth_response(current_user)

      return resp
    return { 'message': 'User already exists.' }, 500


class Login(Resource):

  def post(self):
    args = login_parser().parse_args()
    user = User.find_by_identity(args.username)
    if user and user.authenticated(password=args.password):

      current_user = {
        'username': user.username,
        'role': user.role,
        'email': user.email
      }

      resp = make_auth_response(current_user)

      return resp
    return { "Error": "Something went wrong." }, 401


class Logout(Resource):
  @jwt_required
  def put(self):
    jti = get_raw_jwt()['jti']

    # prevent circular imports
    from felinefolia.blueprints.user.tasks import (set_revoked_token)
    set_revoked_token(jti, 'true')

    resp = make_response()

    set_access_cookies(resp, '') # until i find a more elegant way,
    set_refresh_cookies(resp, '') # just set access token to empty strings
    return resp

class Account(Resource):

  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    print(current_user)
    return current_user, 200

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Account, '/account')
