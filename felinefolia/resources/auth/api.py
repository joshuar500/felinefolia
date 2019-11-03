from flask import (make_response)
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    get_raw_jwt,
    get_jwt_identity
)

from felinefolia.resources.user.models import User
from .helpers import make_auth_response
from .parsers import registration_parser, login_parser


class Register(Resource):

    def post(self):
        args = registration_parser().parse_args()
        found_user = User.find_by_identity(args.email)
        if not found_user:
            user = User(username=args.email, email=args.email)
            user.password = user.encrypt_password(args.password)
            user.save()
            current_user = {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'email': user.email,
                'subscribed': user.subscribed
            }

            from felinefolia.resources.user.tasks import add_subscriber
            add_subscriber(user.email)
            resp = make_auth_response(current_user)
            return resp
        return {'message': 'User already exists.'}, 500


class Login(Resource):

    @jwt_required
    def get(self):
        user = get_jwt_identity()
        if user:
            found_user = User.find_by_identity(user['email'])
            if found_user:
                current_user = {
                    'id': found_user.id,
                    'username': found_user.username,
                    'role': found_user.role,
                    'email': found_user.email,
                    'subscribed': found_user.subscribed
                }
                resp = current_user
                return resp
        return {}, 204

    def post(self):
        args = login_parser().parse_args()
        user = User.find_by_identity(args.username)
        print(user)
        if user and user.authenticated(password=args.password):
            current_user = {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'email': user.email,
                'subscribed': user.subscribed
            }
            resp = make_auth_response(current_user)
            return resp
        return {"Error": "Something went wrong."}, 401


class Logout(Resource):

    @jwt_required
    def put(self):
        jti = get_raw_jwt()['jti']

        # prevent circular imports
        from felinefolia.resources.user.tasks import (set_revoked_token)
        set_revoked_token(jti, 'true')

        resp = make_response()

        set_access_cookies(resp, '')  # until i find a more elegant way,
        set_refresh_cookies(resp, '')  # just set access token to empty strings
        return resp
