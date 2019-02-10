import secrets
import string
import json

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

from lib.util_decorators import admin_required

admin = Blueprint('admin', __name__)
api = Api(admin)

class Dashboard(Resource):

  @jwt_required
  @admin_required
  def get(self):
    group_and_count_comments = Comment.group_and_count_comments()
    return { 'counted_comments': group_and_count_comments }, 200

class Users(Resource):

  @jwt_required
  @admin_required
  @marshal_with(User.__json__())
  def get(self):
    all_users = User.query.all()
    return all_users, 200

api.add_resource(Dashboard, '/dashboard')
api.add_resource(Users, '/users')
