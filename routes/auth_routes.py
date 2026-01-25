from flask import Blueprint, request, jsonify
import bcrypt, jwt
from config import SECRET_KEY
from models.user_model import create_user, find_user_by_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_pw = bcrypt.hashpw(
        data["password"].encode("utf-8"),
        bcrypt.gensalt()
    )

    user = {
        "name": data.get("name"),
        "email": data.get("email"),
        "password": hashed_pw,
        # allow role to be provided by client (owner/customer), default to customer
        "role": data.get("role", "customer")
    }

    # prevent duplicate registration
    existing = find_user_by_email(auth_bp.mongo, user["email"])
    if existing:
        return jsonify({"message": "Email already registered"}), 400

    create_user(auth_bp.mongo, user)

    return jsonify({"message": "Customer registered successfully"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = find_user_by_email(auth_bp.mongo, data["email"])

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        user["password"]
    ):
        return jsonify({"message": "Invalid password"}), 401

    token = jwt.encode(
        {"email": user["email"], "role": user["role"]},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "role": user["role"],
        "email": user["email"],
        "name": user.get("name", "User")
    })
