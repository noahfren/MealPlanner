from flask import *
from app import lm
from app import mongo.db as db
from models import User

login_api = Blueprint('login_api', __name__, template_folder='templates')

@login_api.route('api/v1/login', methods=['POST'])
def login_api_route():
	# Potential errors to return
	errors = []

	if request.method == 'POST':
		payload = request.get_json()

		# Check input
		if not 'username' in req:
			errors.append({"message":"You did not provide a username"})
			return jsonify(errors=errors), 422
		if not 'password' in req:
			errors.append({"message":"You did not provide a password"})
			return jsonify(errors=errors), 422

		username = payload['username']
		password = payload['password']

		user_query = db.users.find_one({"_id": username})
		if not user_query:
			errors.append({"message":"No user with this username exists"})
			return jsonify(errors=errors), 422
		
		user = User(user_query['id'], user_query['password_hash'])
		if user.validate_login(password):
			session['username'] = username
			return jsonify({"username": username}), 201

		errors.append({"message":"Incorrect password"})
		return jsonify(errors=errors), 422