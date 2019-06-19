
from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from .config import app_config
from .models import db, bcrypt

def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if env_name == 'production':
        CORS(app)
        Heroku(app)

    # register blueprints

    bcrypt.init_app(app)
    db.init_app(app)
    
    return app
