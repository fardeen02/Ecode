from app import db

class TestCase(db.Model):
	__test__ =False
	
	__tablename__ = "test_cases"
	
	test_case_id = db.Column(db.Integer, primary_key=True)
	problem_id = db.Column(db.Integer, db.ForeignKey("problems.problem_id"), nullable=False)
	input_data = db.Column(db.Text, nullable=False)
	expected_output = db.Column(db.Text, nullable=False)
	is_public = db.Column(db.Boolean, nullable=False, default=False)
	test_case_order = db.Column(db.Integer, nullable=False)
	
	problem = db.relationship(
	"Problem", 
	back_populates="test_cases"
	)