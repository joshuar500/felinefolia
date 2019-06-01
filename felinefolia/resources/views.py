from flask import Blueprint
from flask_restful import Api

from felinefolia.resources.auth import (Register, Login, Logout)
from felinefolia.resources.user import (UserResource)
from felinefolia.resources.contact import (Contact)
from felinefolia.resources.billing import (Subscribe)
from felinefolia.resources.admin import (Dashboard, AdminUserList)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


# Auth Resources
api.add_resource(UserResource, '/users/<int:user_id>')

# User Resources
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

# Contact Resources
api.add_resource(Contact, '/contact')

# Billing Resources
api.add_resource(Subscribe, '/subscribe')

# Admin Resources
api.add_resource(Dashboard, '/dashboard')
api.add_resource(AdminUserList, '/users')
