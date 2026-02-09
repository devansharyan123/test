from flask import Blueprint, request, jsonify
from Database.models import User, Base
from Database.database import SessionLocal, engine
import jwt
import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

SECRET_KEY = "your_secret_key_here"

# Create tables if not exist
Base.metadata.create_all(bind=engine)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    auth_header = request.headers.get("Authorization")

    with SessionLocal() as session:
        user_count = session.query(User).count()

        if user_count > 0:
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Authorization token required"}), 401

            token = auth_header.split()[1]
            try:
                jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except:
                return jsonify({"error": "Invalid token"}), 401

        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()

        return jsonify({
            "message": f"User {username} created successfully",
            "user_id": new_user.id
        })

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.password != password:
            return jsonify({"error": "Wrong password"}), 401

        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "message": f"Welcome {username}!",
            "user_id": user.id,
            "token": token
        })
