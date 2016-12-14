from flask import *
from flask.ext.login import logout_user
from app import lm
from app import mongo.db as db
from models import User

logout_api = Blueprint('logout_api', __name__, template_folder='templates')

@login_api.route('api/v1/logout', methods=['POST'])
def logout_api_route():
	errors = []
	if 'username' not in session:
		errors.append({"message":"You do not have the necessary credentials for this resource"})
		return jsonify(errors=errors), 401

	session.pop('username', None)
	return 204