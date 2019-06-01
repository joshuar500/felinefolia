from flask import (make_response)
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    get_raw_jwt
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
            print('im right here')
            current_user = {
                'username': user.username,
                'role': user.role,
                'email': user.email
            }

            from felinefolia.resources.user.tasks import add_subscriber
            add_subscriber(user.email)
            print('lol im right here')
            resp = make_auth_response(current_user)
            print('jkjk im right here')
            return resp
        return {'message': 'User already exists.'}, 500


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
            print(current_user)

            resp = make_auth_response(current_user)
            print('~~~~~~~~~~~~~~~~~~~~~|||||||||')
            print(resp.json)
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
