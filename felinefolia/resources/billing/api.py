from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from felinefolia.resources.billing.models.subscription import Subscription

register_parser = reqparse.RequestParser()
register_parser.add_argument(
    'id'
)


class Subscribe(Resource):
    """
    Create a monthly subscription for a user


    """
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        args = register_parser.parse_args()
        print(args.id)
        from felinefolia.resources.user.models import User
        user = User.find_by_identity(current_user['username'])
        if user and user.subscription:
            print('User has a subscription!')
        print('User does not have a subscription!')
        # TODO:
        # 1. get the plan from args
        subscription_plan = Subscription.get_plan_by_id(0)
        print(subscription_plan)  # remove this print
        # 2. guard against invalid plan
        # 3. get user, create plan
        subscription = Subscription()
        created = subscription.create(user=user,
                                      name='joshua rincon',
                                      plan=0,
                                      coupon=None,
                                      token=args.id)
        if created:
            print('something great happened!')
        else:
            print('something bad happened!')

        return current_user, 200
