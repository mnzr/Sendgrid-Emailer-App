import os
from flask import Flask

project_root = os.path.dirname(os.path.realpath(__file__))
uploads = os.path.join(os.pardir, 'tmp')
template_path = os.path.join(project_root, 'templates')
# Creates an object called app of Flask class
app = Flask(__name__, template_folder=template_path, instance_relative_config=True)
app.config.from_object('config')
app.config['UPLOADS'] = uploads
app.config['DEBUG'] = True

# Imports app package from views, not the same as object 'app'
from app import views
