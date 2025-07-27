from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db
from models.user import User
from models.pending_user import PendingUser

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# ✅ Login Route (Admin + User)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if user.role == "admin":
        token = create_access_token(identity={"email": user.email, "role": "admin"})
        return jsonify({"token": token, "email": user.email, "role": "admin"}), 200

    if not user.approved:
        return jsonify({"error": "Account not approved by admin yet"}), 403

    token = create_access_token(identity={"email": user.email, "role": "user"})
    return jsonify({"token": token, "email": user.email, "role": "user"}), 200

# ✅ Get current logged-in user
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identity = get_jwt_identity()
    return jsonify(identity), 200

# ✅ Signup route (user must be approved by admin)
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password or not full_name:
        return jsonify({"msg": "Missing required fields"}), 400

    if PendingUser.query.filter_by(email=email).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "You already signed up or have an account."}), 400

    pending = PendingUser(email=email, full_name=full_name, password=password)
    db.session.add(pending)
    db.session.commit()
    return jsonify({"msg": "Signup submitted. Await admin approval."}), 200

# ✅ Admin-only: view pending users
@auth_bp.route("/pending-users", methods=["GET"])
@jwt_required()
def get_pending_users():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"msg": "Access denied"}), 403

    users = PendingUser.query.all()
    return jsonify([
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name
        } for u in users
    ]), 200

# ✅ Admin-only: approve a pending user
@auth_bp.route("/approve-user/<int:user_id>", methods=["POST"])
@jwt_required()
def approve_user(user_id):
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"msg": "Admin access required"}), 403

    pending = PendingUser.query.get(user_id)
    if not pending:
        return jsonify({"msg": "User not found"}), 404

    new_user = User(
        full_name=pending.full_name,
        email=pending.email,
        password=pending.password,
        role="user",
        approved=True
    )
    db.session.add(new_user)
    db.session.delete(pending)
    db.session.commit()
    return jsonify({"msg": f"Approved {pending.email}"}), 200
