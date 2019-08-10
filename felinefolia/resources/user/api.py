from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    # get_jwt_identity
)

from .models import User


class UserResource(Resource):

    @jwt_required
    def get(self, user_id):
        # current_user = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        if user:
            return user.as_dict(), 200
        return {"user": "not found"}, 404
