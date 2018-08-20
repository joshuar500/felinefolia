from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    url_for,
    jsonify,
    render_template)
from flask_restful import Api, Resource, url_for
from flask_restful.utils import cors

contact = Blueprint('api', __name__)
api = Api(contact)

class Contact(Resource):

  @cors.crossdomain(origin='*')
  def get(self):
    resp = { 'message': 'here is some data' }
    return jsonify(resp)


api.add_resource(Contact, '/contact')
