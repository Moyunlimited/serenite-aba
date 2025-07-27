from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.quiz_progress import QuizProgress
from db import db
from datetime import datetime

progress_bp = Blueprint("progress", __name__, url_prefix="/api/progress")

@progress_bp.route("/", methods=["POST"])
@jwt_required()
def save_progress():
    data = request.get_json()
    identity = get_jwt_identity()

    progress = QuizProgress(
        email=identity["email"],
        quiz_id=data["quiz_id"],
        score=data["score"],
        total=data["total"],
        timestamp=datetime.now(),
        quiz_title=data.get("quiz_title", "")
    )

    db.session.add(progress)
    db.session.commit()
    return jsonify({"message": "Progress saved"}), 201

@progress_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_progress():
    identity = get_jwt_identity()
    progresses = QuizProgress.query.filter_by(email=identity["email"]).all()
    return jsonify([p.serialize() for p in progresses]), 200
