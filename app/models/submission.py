from datetime import datetime, UTC
from app import db

class Submission(db.Model):
	__tablename__ = "submissions" 
	
	submission_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	problem_id = db.Column(db.Integer, db.ForeignKey("problems.problem_id"), nullable=False)
	language = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(100), nullable=False)
	execution_time = db.Column(db.Integer, nullable=False)
	submitted_at = db.Column(db.DateTime, default=lambda:datetime.now(UTC), nullable=False)
	