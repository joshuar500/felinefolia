from flask_restful import Resource, reqparse, fields
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from felinefolia.resources.billing.models.subscription import Subscription

address_fields = {}
address_fields['line 1'] = fields.String(attribute='addr1')
address_fields['line 2'] = fields.String(attribute='addr2')
address_fields['city'] = fields.String(attribute='city')
address_fields['state'] = fields.String(attribute='state')
address_fields['zip'] = fields.String(attribute='zip')


register_parser = reqparse.RequestParser()
register_parser.add_argument('productPlan')
register_parser.add_argument('name')
register_parser.add_argument('tokenId')
register_parser.add_argument('address', type=dict)
register_parser.add_argument('shipping', type=dict)


class Subscribe(Resource):
    """
    Create a monthly subscription for a user


    """
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        args = register_parser.parse_args()
        # prevent circular imports
        from felinefolia.resources.user.models import User
        user = User.find_by_identity(current_user['username'])
        if user and user.subscription:
            return {'message': 'User already subscribed to a plan.'}, 400
        # Do we need this 👇
        # subscription_plan = Subscription.get_plan_by_id(args.productPlan)
        # TODO: Guard against invalid plan?
        subscription = Subscription()
        created = subscription.create(user=user,
                                      name=args.name,
                                      plan=args.productPlan,
                                      coupon=None,
                                      token=args.tokenId,
                                      address=args.address,
                                      shipping=args.shipping)

        if created:
            return {'message': 'Subscribed'}
        else:
            return {'message': 'Something went wrong. Please contact hello@felinefolia.com'}

        return current_user, 200


class Unsubscribe(Resource):
    """
    Deletes a monthly subscription for a user

    """

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        # args = register_parser.parse_args()
        # prevent circular imports
        from felinefolia.resources.user.models import User
        user = User.find_by_identity(current_user['username'])
        if user and user.subscription:
            subscription = Subscription()
            cancelled = subscription.cancel(user=user)

        if cancelled:
            return {'message': 'Subscription Cancelled'}
        else:
            return {'message': 'Something went wrong. Please contact hello@felinefolia.com'}

        return current_user, 200
