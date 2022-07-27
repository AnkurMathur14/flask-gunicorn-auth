import os
import flask
import flask_restful
#from flask_sqlalchemy import SQLAlchemy

from resources.users import User, UserList
from resources.filesystems import FileSystem, FileSystemList
from resources.authentication import Authentication

# Creating a Flask app
app = flask.Flask(__name__)

# Setting secret key in application context
SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
app.config['SECRET_KEY'] = SECRET_KEY

# Creating a blueprint object
policyapi_bp = flask.Blueprint('policyapi', __name__)
policyapi = flask_restful.Api(policyapi_bp)

# Adding a resource with corresponding URL
policyapi.add_resource(UserList, '/users')
policyapi.add_resource(User, '/users/<user_id>')

policyapi.add_resource(FileSystemList, '/filesystems')
policyapi.add_resource(FileSystem, '/filesystems/<fs_id>')

policyapi.add_resource(Authentication, '/login')

# Registering the blueprint with the appliacation
app.register_blueprint(policyapi_bp, url_prefix='/api/v1')

