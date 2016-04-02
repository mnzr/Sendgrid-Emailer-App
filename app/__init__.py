import os
from flask import Flask

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
# Creates an object called app of Flask class
app = Flask(__name__, template_folder=template_path)
app.config.from_object('config')

# Imports app package from views, not the same as object 'app'
from app import views
