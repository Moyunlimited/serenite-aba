from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.quiz import Quiz
from db import db

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api/quiz")

@quiz_bp.route("/", methods=["GET"])
def get_quizzes():
    quizzes = Quiz.query.all()
    return jsonify([q.serialize() for q in quizzes]), 200

@quiz_bp.route("/", methods=["POST"])
@jwt_required()
def create_quiz():
    data = request.get_json()
    title = data.get("title")
    questions = data.get("questions")

    if not isinstance(title, str):
        return jsonify({"error": "Title must be a string"}), 422
    if not isinstance(questions, list):
        return jsonify({"error": "Questions must be a list"}), 422

    quiz = Quiz(title=title, questions=questions)
    db.session.add(quiz)
    db.session.commit()
    return jsonify(quiz.serialize()), 201

@quiz_bp.route("/<int:quiz_id>", methods=["PUT"])
@jwt_required()
def update_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    data = request.get_json()
    quiz.title = data.get("title", quiz.title)
    quiz.questions = data.get("questions", quiz.questions)

    db.session.commit()
    return jsonify(quiz.serialize()), 200

@quiz_bp.route("/<int:quiz_id>", methods=["DELETE"])
@jwt_required()
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"msg": "Quiz deleted"}), 200
