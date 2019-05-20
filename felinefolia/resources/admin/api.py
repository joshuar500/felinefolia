from flask_restful import Resource, marshal_with
from flask_jwt_extended import (
    jwt_required
)

from felinefolia.resources.user.models import User
from felinefolia.resources.contact.models import Comment

from lib.util_decorators import admin_required


class Dashboard(Resource):

    @jwt_required
    @admin_required
    def get(self):
        group_and_count_comments = Comment.group_and_count_comments()
        return {'counted_comments': group_and_count_comments}, 200


class Users(Resource):

    @jwt_required
    @admin_required
    @marshal_with(User.__json__())
    def get(self):
        all_users = User.query.all()
        return all_users, 200
