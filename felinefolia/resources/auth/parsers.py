from flask_restful import reqparse


def email_validation(email_str):
    """Return email_str if valid, raise an exception in other case."""
    # if valid_email(email_str):
    #     return email_str
    # else:
    #     raise ValueError('{} is not a valid email'.format(email_str))
    return email_str


def registration_parser():

    register_parser = reqparse.RequestParser()
    register_parser.add_argument(
        'email', dest='email',
        type=email_validation,
        required=True, help='The user\'s email',
    )
    register_parser.add_argument(
        'password', dest='password',
        required=True, help='The user\'s password',
    )
    register_parser.add_argument(
        'user_priority', dest='user_priority',
        type=int,
        default=1, choices=range(5), help='The user\'s priority',
    )

    return register_parser


def login_parser():
    login_parser = reqparse.RequestParser()
    login_parser.add_argument('username', required=True)
    login_parser.add_argument('password', required=True)
    return login_parser
