from app import db

class Problem(db.Model):
	__tablename__ = "problems"
	
	problem_id = db.Column(db.Integer, primary_key=True)
	day_number = db.Column(db.Integer, unique=True, nullable=False)
	topic = db.Column(db.String(250), nullable=False)
	sub_topic = db.Column(db.String(250), nullable=False)
	difficulty = db.Column(db.Integer, nullable=False)
	title = db.Column(db.Text, nullable=False)
	description = db.Column(db.Text, nullable=False)
	input_format = db.Column(db.Text, nullable=False)
	output_format = db.Column(db.Text, nullable=False)
	constraints = db.Column(db.Text, nullable=False)
	time_limit = db.Column(db.Integer, nullable=False)
	
	test_cases = db.relationship(
	             "TestCase", 
				 back_populates="problem", 
				 cascade="all, delete-orphan", 
				 order_by="TestCase.test_case_order"
				 )
				 