from functools import wraps

from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims
)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return {'message': 'Admins only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def add_user_claims_loader(jwt):
    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {'role': user['role']}
