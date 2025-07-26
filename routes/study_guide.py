from flask import Blueprint, request, jsonify
from models.topic import Topic
from db import db

guide_bp = Blueprint("guide", __name__, url_prefix="/api/guide")

# 🔹 Get all topics
@guide_bp.route("/", methods=["GET"])
def get_topics():
    topics = Topic.query.all()
    return jsonify([t.serialize() for t in topics]), 200

# 🔹 Add a new topic
@guide_bp.route("/", methods=["POST"])
def add_topic():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Missing fields"}), 400

    new_topic = Topic(title=title, content=content)
    db.session.add(new_topic)
    db.session.commit()
    return jsonify(new_topic.serialize()), 201

# 🔹 Delete topic by ID
@guide_bp.route("/<int:id>", methods=["DELETE"])
def delete_topic(id):
    topic = Topic.query.get(id)
    if not topic:
        return jsonify({"error": "Topic not found"}), 404

    db.session.delete(topic)
    db.session.commit()
    return jsonify({"msg": "Deleted"}), 200

# 🔹 Edit topic by ID
@guide_bp.route("/<int:id>", methods=["PUT"])
def update_topic(id):
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    topic = Topic.query.get(id)
    if not topic:
        return jsonify({"error": "Topic not found"}), 404

    topic.title = title
    topic.content = content
    db.session.commit()

    return jsonify(topic.serialize()), 200
