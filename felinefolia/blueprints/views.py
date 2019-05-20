from flask import Blueprint
from flask_restful import Api
from felinefolia.blueprints.user import (Register, Login, Logout, Account)
from felinefolia.blueprints.contact import (Contact)
from felinefolia.blueprints.billing import (Subscribe)
from felinefolia.blueprints.admin import (Dashboard, Users)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


# User Resources
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Account, '/account')


# Contact Resources
api.add_resource(Contact, '/contact')

# Billing Resources
api.add_resource(Subscribe, '/subscribe')

# Admin Resources
api.add_resource(Dashboard, '/dashboard')
api.add_resource(Users, '/users')
