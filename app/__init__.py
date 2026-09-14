from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=None):
	app = Flask(__name__)
	
	app.config.from_object(config_class or Config)
	
	db.init_app(app)
	bcrypt.init_app(app)
	jwt.init_app(app)
	
	from app.models.user import User
	from app.routes.auth import auth_bp
	
	app.register_blueprint(auth_bp)
	
	return app
	
	