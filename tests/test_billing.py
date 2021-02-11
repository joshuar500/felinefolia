import stripe

stripe.api_key = 'sk_test_nIRds9NsBCaZVRrfy28UD6xX'


def test_subscribe(app, client, db, member_json_access_token):
    token = stripe.Token.create(
        card={
            "number": '4242424242424242',
            "exp_month": 12,
            "exp_year": 2022,
            "cvc": '123'
        },
    )

    request_payload = {
        'productPlan': 'plan_Fb9pnxV1emnn3h',
        'tokenId': token.id,
        'name': 'John Smith',
        'address': {
            'city': "Long Beach",
            'country': 'US',
            'line1': '333 Newport Ave',
            'line2': 'Apt 303',
            'postal_code': '90814',
            'state': 'CA'
        },
        'shipping': {
            'name': 'Joshua Rincon',
            'address': {
                'city': "Long Beach",
                'country': 'US',
                'line1': '333 Newport Ave',
                'line2': 'Apt 303',
                'postal_code': '90814',
                'state': 'CA'
            }
        },
        **member_json_access_token
    }
    rep = client.post('/api/v1/subscribe', json=request_payload)
    return None


def test_unsubscribe(app, client, db, member_json_access_token):
    token = stripe.Token.create(
        card={
            "number": '4242424242424242',
            "exp_month": 12,
            "exp_year": 2022,
            "cvc": '123'
        },
    )

    # @id: the plan id
    request_payload = {
        'productPlan': 'plan_Fb9pnxV1emnn3h',
        'tokenId': token.id,
        'name': 'John Smith',
        'address': {
            'city': "Long Beach",
            'country': 'US',
            'line1': '333 Newport Ave',
            'line2': 'Apt 303',
            'postal_code': '90814',
            'state': 'CA'
        },
        'shipping': {
            'name': 'Joshua Rincon',
            'address': {
                'city': "Long Beach",
                'country': 'US',
                'line1': '333 Newport Ave',
                'line2': 'Apt 303',
                'postal_code': '90814',
                'state': 'CA'
            }
        },
        **member_json_access_token
    }
    # First subscribe a user
    rep1 = client.post('/api/v1/subscribe', json=request_payload)

    # Then cancel the user's subscription
    rep2 = client.post('/api/v1/unsubscribe', json=request_payload)
    return None
