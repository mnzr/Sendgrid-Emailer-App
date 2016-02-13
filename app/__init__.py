import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config
# Creates an object called app of Flask class
app = Flask(__name__)
app.config.from_object('config')
# for database
db = SQLAlchemy(app)

# Imports app package from views, not the same as object 'app'
from app import views, models
