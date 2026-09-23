from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.problem import Problem
from app import db

problems_bp = Blueprint("problems",__name__, url_prefix="/api/problems")

@problems_bp.route("/<int:problem_id>", methods=["GET"])
@jwt_required()
def get_problem(problem_id):
	problem = db.session.get(Problem, problem_id)
	
	if not problem:
		return jsonify({
		     "error": "Problem not found"
		}), 404
		
	return jsonify({
		"problem_id": problem.problem_id,
		"day_number": problem.day_number,
		"topic": problem.topic,
		"difficulty": problem.difficulty,
		"title": problem.title,
		"description": problem.description,
		"input_format": problem.input_format,
		"output_format": problem.output_format,
		"constraints": problem.constraints,
		"time_limit": problem.time_limit
		}), 200