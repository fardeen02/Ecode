from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)
from app import db, bcrypt
from app.models.user import User

auth_bp = Blueprint("auth",__name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
	data = request.get_json()
	
	if not data:
		return jsonify({
          "error" : "Request body is required"		
		}), 400
		
	username = data.get("username")
	
	if not username:
		return jsonify({
          "error" : "Username is required"		
		}), 400
		
	existing_username = User.query.filter_by(username=username).first()
		
	if existing_username:
		return jsonify({
          "error" : "Username is already exists"		
		}), 409
		
	email = data.get("email")
	
	if not email:
		return jsonify({
          "error" : "Email is required"		
		}), 400
	
	existing_email = User.query.filter_by(email=email).first()
    
	if existing_email:
		return jsonify({
          "error" : "Email is already exists"		
		}), 409
		
	password = data.get("password")
	
	if not password:
		return jsonify({
          "error" : "Password is required"		
		}), 400
		
	preferred_language = data.get("preferred_language")
	
	if not preferred_language:
		return jsonify({
          "error" : "Preferred Language is required"		
		}), 400
	
	hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
	
	user = User(
	    username=username,
		email=email,
		password=hashed_password,
		preferred_language=preferred_language
	)
	
	db.session.add(user)
	db.session.commit()
	
	return jsonify({
	    "message": f"User: {username} is registered successfully",
		"user":{
		   "user_id": user.user_id,
		   "username": username,
		   "email": email,
		   "preferred_language": preferred_language
		}
	}), 201
	
@auth_bp.route("/login", methods=["POST"])
def login():
	data = request.get_json()
	
	if not data:
		return jsonify({
		   "error" : "Request body is required"
		}), 400
	
	username = data.get("username")
	password = data.get("password")
	
	if not username or not password:
		return jsonify({
		   "error" : "Username and Password are required"
		}), 400
	
	user = User.query.filter_by(username=username).first()
	
	if not user:
		return jsonify({
		     "error": "Invalid username or password"
		}), 401
		
	if not bcrypt.check_password_hash(user.password, password):
		return jsonify({
		     "error": "Invalid username or password"
		}), 401
		
	access_token = create_access_token(identity=str(user.user_id))
	
	return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
		    "user_id": user.user_id,
			"username": user.username,
			"email": user.email,
			"preferred_language": user.preferred_language
		}		
	}), 200
		
	