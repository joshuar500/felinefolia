from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from .models import User


class UserResource(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        user = User.find_by_identity(current_user['username'])
        if user:
            print(user.as_dict())
            return user.as_dict(), 200
        return {"Error": "Failed to get account."}, 401
