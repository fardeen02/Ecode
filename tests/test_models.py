import pytest

from app import create_app, db
from app.models.problem import Problem
from app.models.testcase import TestCase
from app.models.submission import Submission
from app.models.user import User 

@pytest.fixture
def app():
	app = create_app()
	
	app.config.update(
	     TESTING=True,
		 SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
	)
	
	with app.app_context():
		db.create_all()
		yield app
		db.session.remove()
		db.drop_all()
		
@pytest.fixture
def client(app):
	return app.test_client()
	
def test_problem_can_have_test_cases(app):
	problem = Problem(
	    day_number=1,
		topic="Java Foundations",
		sub_topic="Variables",
		difficulty=1,
		title="Calculate a Sum",
		description="Calcute the sum of two numbers.",
		input_format="Two integers.",
		output_format="Print sum.",
		constraints="The integers are within the allowed range.",
		time_limit=1000
	)
	
	db.session.add(problem)
	db.session.commit()
	
	test_case = TestCase(
	    problem_id=problem.problem_id,
		input_data="5 7",
		expected_output="12",
		is_public=True,
		test_case_order=1
	)
	
	db.session.add(test_case)
	db.session.commit()
	
	assert len(problem.test_cases) == 1
	assert problem.test_cases[0].expected_output == "12"


def test_test_case_belongs_to_problem(app):
	problem = Problem(
	    day_number=2,
		topic="Java Foundations",
		sub_topic="Arithmetic",
		difficulty=1,
		title="Calculate Product",
		description="Calcute the product of two numbers.",
		input_format="Two integers.",
		output_format="Print their product.",
		constraints="The integers are within the allowed range.",
		time_limit=1000
	)
	
	db.session.add(problem)
	db.session.commit()
	
	test_case = TestCase(
	    problem_id=problem.problem_id,
		input_data="4 5",
		expected_output="20",
		is_public=True,
		test_case_order=1
	)
	
	db.session.add(test_case)
	db.session.commit()
	
	assert test_case.problem.problem_id == problem.problem_id
	assert test_case.problem.title == "Calculate Product"


def test_test_cases_are_ordered(app):
	problem = Problem(
	    day_number=3,
		topic="Decision Making",
		sub_topic="If Statement",
		difficulty=2,
		title="Check Number",
		description="Check a Number",
		input_format="one integer.",
		output_format="Print the result",
		constraints="The input is an integer.",
		time_limit=1000
	)
	
	db.session.add(problem)
	db.session.commit()
	
	for order in [5, 2, 4, 1, 3]:
		db.session.add(
		    TestCase(
			    problem_id=problem.problem_id,
				input_data=str(order),
				expected_output=str(order),
				is_public=(order == 1),
				test_case_order=order
				)
	    )
	
	db.session.commit()
	
	orders = [
	    test_case.test_case_order
		for test_case in problem.test_cases
	]
	
	assert orders == [1, 2, 3, 4, 5]


def test_public_and_hidden_test_cases(app):
    problem = Problem(
        day_number=4,
        topic="Loops",
        sub_topic="For Loop",
        difficulty=3,
        title="Count Numbers",
        description="Count numbers.",
        input_format="An integer.",
        output_format="Print the count.",
        constraints="The input is positive.",
        time_limit=1000
    )

    db.session.add(problem)
    db.session.commit()

    public_case = TestCase(
        problem_id=problem.problem_id,
        input_data="5",
        expected_output="5",
        is_public=True,
        test_case_order=1
    )

    hidden_case = TestCase(
        problem_id=problem.problem_id,
        input_data="100",
        expected_output="100",
        is_public=False,
        test_case_order=2
    )

    db.session.add_all([public_case, hidden_case])
    db.session.commit()

    assert public_case.is_public is True
    assert hidden_case.is_public is False
	
def test_deleting_problem_deletes_test_cases(app):
    problem = Problem(
        day_number=5,
        topic="Strings",
        sub_topic="String Basics",
        difficulty=3,
        title="String Test",
        description="Process a string.",
        input_format="A string.",
        output_format="Print the result.",
        constraints="The string is valid.",
        time_limit=1000
    )

    db.session.add(problem)
    db.session.commit()

    test_case = TestCase(
        problem_id=problem.problem_id,
        input_data="hello",
        expected_output="hello",
        is_public=True,
        test_case_order=1
    )

    db.session.add(test_case)
    db.session.commit()

    test_case_id = test_case.test_case_id

    db.session.delete(problem)
    db.session.commit()

    deleted_case = db.session.get(TestCase, test_case_id)

    assert deleted_case is None
	

def test_day_number_must_be_unique(app):
    problem_1 = Problem(
        day_number=6,
        topic="Arrays",
        sub_topic="Basics",
        difficulty=4,
        title="Array Test One",
        description="Test.",
        input_format="An array.",
        output_format="Print the result.",
        constraints="Valid array.",
        time_limit=1000
    )

    problem_2 = Problem(
        day_number=6,
        topic="Arrays",
        sub_topic="Traversal",
        difficulty=4,
        title="Array Test Two",
        description="Test.",
        input_format="An array.",
        output_format="Print the result.",
        constraints="Valid array.",
        time_limit=1000
    )

    db.session.add(problem_1)
    db.session.commit()

    db.session.add(problem_2)

    with pytest.raises(Exception):
        db.session.commit()

    db.session.rollback()
	

def test_submission_belongs_to_user_and_problem(app):
    with app.app_context():
        user = User(
            username="submission_user",
            email="submission@example.com",
            password="hashed_password",
            preferred_language="Python"
        )

        problem = Problem(
            day_number=1,
            topic="Java Foundations",
            sub_topic="Variables",
            difficulty=1,
            title="Test Problem",
            description="Test description",
            input_format="Input",
            output_format="Output",
            constraints="None",
            time_limit=1000
        )

        db.session.add(user)
        db.session.add(problem)
        db.session.commit()

        submission = Submission(
            user_id=user.user_id,
            problem_id=problem.problem_id,
            language="Python",
            status="accepted",
            execution_time=125
        )

        db.session.add(submission)
        db.session.commit()

        assert submission.user_id == user.user_id
        assert submission.problem_id == problem.problem_id


def test_submission_stores_result_metadata(app):
    with app.app_context():
        user = User(
            username="result_user",
            email="result@example.com",
            password="hashed_password",
            preferred_language="Python"
        )

        problem = Problem(
            day_number=2,
            topic="Decision Making",
            sub_topic="if",
            difficulty=2,
            title="Test Problem",
            description="Test description",
            input_format="Input",
            output_format="Output",
            constraints="None",
            time_limit=1000
        )

        db.session.add_all([user, problem])
        db.session.commit()

        submission = Submission(
            user_id=user.user_id,
            problem_id=problem.problem_id,
            language="Java",
            status="wrong_answer",
            execution_time=250
        )

        db.session.add(submission)
        db.session.commit()

        saved = Submission.query.first()

        assert saved.language == "Java"
        assert saved.status == "wrong_answer"
        assert saved.execution_time == 250
        assert saved.submitted_at is not None


	










