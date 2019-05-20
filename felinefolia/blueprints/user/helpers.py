from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    set_access_cookies,
    set_refresh_cookies,
)


def make_auth_response(current_user):

    access_token = create_access_token(identity=current_user)
    refresh_token = create_refresh_token(identity=current_user)

    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)

    # prevent circular imports
    from felinefolia.blueprints.user.tasks import (set_revoked_token)
    set_revoked_token(access_jti, 'false')
    set_revoked_token(refresh_jti, 'false')

    # prevent circular imports
    from flask import make_response
    resp = make_response()

    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp
