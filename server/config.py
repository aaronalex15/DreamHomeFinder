# Standard library imports
import os

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instantiate app, set attributes
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.secret_key = os.environ.get("SESSION_SECRET")
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"

# SQLAlchemy setup
db = SQLAlchemy(app)
app.config["SESSION_SQLALCHEMY"] = db
migrate = Migrate(app, db)

# REST API setup
api = Api(app)

# CORS setup
CORS(app)

# Bcrypt setup
flask_bcrypt = Bcrypt(app)

# Session setup
session = Session(app)
