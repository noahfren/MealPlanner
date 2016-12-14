from flask import *
from werkzeug.security import check_password_hash, generate_password_hash
from app import lm
from app import mongo.db as db
from models import User

user_api = Blueprint('user_api', __name__, template_folder='templates')

@user_api.route('api/v1/user',methods=['GET', 'POST', 'PUT'])
def user_api_route():

	#List of potential errors to return
	errors = []

	# Check if client is logged in
	if request.method == 'GET':
		if 'username' in session:
			user = lm.current_user
			return 
		else:
			errors.append({"message":"You do not have the necessary credentials for the resource"})
			return jsonify(errors=errors), 401

	# Create new user
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

		users = db.users.find({"_id": username})
		if len(users) != 0:
			errors.append({"message":"This username is taken"})
			return jsonify(errors=errors), 422

		# Create new user in db
		password_hash = generate_password_hash(password)
		db.users.insert_one({
			'_id': username,
			'password_hash': password_hash
		})

		return jsonify({'username': username}), 201