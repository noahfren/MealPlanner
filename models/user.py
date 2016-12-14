from flask import *
from app import lm
from app import mongo.db as db
from werkzeug.security import check_password_hash

@lm.user_loader
def load_user(user_id):
	user = db.users.find_one({"_id": user_id})
	if not user:
		return None
	return User(user["_id"], user["password_hash"])

class User():
	"""Class to represent users in MealPlanner"""
	def __init__(self, username, pw_hash):
		self.username = username
		self.password_hash = pw_hash

	def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def validate_login(password):
        return check_password_hash(self.password_hash, password)