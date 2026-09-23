from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User
from app.models.problem import Problem

def create_user():
	return User(
		username="problem_user",
		email="problem@example.com",
		password="hashed_password",
		preferred_language="Python"
	)
	
def create_problem():
	return Problem(
		day_number=1,
		topic="Java Foundations",
		sub_topic="Variables",
		difficulty=1,
		title="Test Problem",
		description="Test description",
		input_format="Input",
		output_format="Output",
		constraints="None",
		time_limit=10000
	)
	
def test_get_problem_requires_authentication(client):
	response = client.get("/api/problems/1")
	
	assert response.status_code == 401
	
def test_get_problem_returns_problem(client, app):
	with app.app_context():
		user = create_user()
		problem = create_problem()
		
		db.session.add_all([user, problem])
		db.session.commit()
		
		token = create_access_token(identity=str(user.user_id))
		
		response = client.get(
			f"/api/problems/{problem.problem_id}",
			headers={
				"Authorization": f"Bearer {token}"
			}
		)
		
		assert response.status_code == 200
		
		data = response.get_json()
		
		assert data["problem_id"] == problem.problem_id
		assert data["day_number"] == 1
		assert data["topic"] == "Java Foundations"
		assert data["difficulty"] == 1
		assert data["title"] == "Test Problem"
		
def test_get_problem_does_not_expose_hidden_data(client, app):
	with app.app_context():
		user = create_user()
		problem = create_problem()
		
		db.session.add_all([user, problem])
		db.session.commit()
		
		token = create_access_token(identity=str(user.user_id))
		
		response = client.get(
		f"/api/problems/{problem.problem_id}",
		headers={
			"Authorization": f"Bearer {token}"
			}
		)
		
		assert response.status_code == 200
		
		data = response.get_json()
		
		assert "sub_topic" not in data
		assert "test_cases" not in data
		assert "expected_output" not in data
		assert "is_public" not in data

def test_get_problem_returnd_404_for_unknown_problem(client, app):
	with app.app_context():
		user = create_user()
		
		db.session.add(user)
		db.session.commit()
		
		token = create_access_token(identity=str(user.user_id))
		
		response = client.get(
			"/api/problems/999999",
			headers={
				"Authorization": f"Bearer {token}"
			}
		)
	
		