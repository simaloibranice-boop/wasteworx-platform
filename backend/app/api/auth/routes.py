from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User, Role


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}

    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role_name = data.get("role", "").strip()

    if not first_name or not last_name or not email or not password or not role_name:
        return {
            "message": "first_name, last_name, email, password and role are required"
        }, 400

    if len(password) < 8:
        return {
            "message": "Password must be at least 8 characters"
        }, 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {
            "message": "A user with this email already exists"
        }, 409

    role = Role.query.filter_by(name=role_name).first()

    if not role:
        return {
            "message": "Invalid role"
        }, 400

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=role,
    )

    user.set_password(password)

    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "message": "Unable to create user"
        }, 400

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role.name,
        },
    }, 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return {
            "message": "Email and password are required"
        }, 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {
            "message": "Invalid email or password"
        }, 401

    if not user.is_active:
        return {
            "message": "User account is inactive"
        }, 403

    access_token = create_access_token(
        identity=str(user.id)
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role.name,
        },
    }, 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return {
            "message": "User not found"
        }, 404

    return {
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role.name,
            "is_active": user.is_active,
        }
    }, 200
