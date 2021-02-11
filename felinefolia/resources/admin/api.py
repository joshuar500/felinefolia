from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required
)

from felinefolia.resources.user.models import User
from felinefolia.resources.contact.models import Comment
from felinefolia.extensions import ma, db

from lib.util_decorators import admin_required


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session


class Dashboard(Resource):

    @jwt_required
    @admin_required
    def get(self):
        group_and_count_comments = Comment.group_and_count_comments()
        return {'counted_comments': group_and_count_comments}, 200


class AdminUserList(Resource):

    @jwt_required
    @admin_required
    def get(self):
        schema = UserSchema()
        users = User.query.all()
        return {"user": schema.dump(users).data}
