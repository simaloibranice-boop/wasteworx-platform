from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import User


def permission_required(permission_name):
    def decorator(function):
        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.session.get(User, int(user_id))

            if not user:
                return jsonify({
                    "message": "User not found"
                }), 404

            if not user.is_active:
                return jsonify({
                    "message": "User account is inactive"
                }), 403

            user_permissions = {
                permission.name
                for permission in user.role.permissions
            }

            if permission_name not in user_permissions:
                return jsonify({
                    "message": "You do not have permission to perform this action"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator
