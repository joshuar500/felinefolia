from flask import jsonify
from flask_restful import Resource
from flask_restful.utils import cors


class Contact(Resource):

    @cors.crossdomain(origin='*')
    def get(self):
        resp = {'message': 'here is some data'}
        return jsonify(resp)
