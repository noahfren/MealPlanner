from flask import Flask
import extensions
import controllers
from flask.ext.pymongo import Pymongo
from flask.ext.login import LoginManager
import config
import api


# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')
app.secret_key = config.env['secret_key']

# Initialize PyMongo and LoginManager
mongo = Pymongo(app)
lm = LoginManager()
lm.init_app(app)


#Blueprints for login, user and logout api
app.register_blueprint(api.user_api, url_prefix='/')
app.register_blueprint(api.login_api, url_prefix='/')
app.register_blueprint(api.logout_api, url_prefix='/')

if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)