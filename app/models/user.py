from datetime import datetime, UTC
from app import db

class User(db.Model):
	__tablename__ = "users"
	
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	preferred_language = db.Column(db.String(50), nullable=False)
	created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False) 