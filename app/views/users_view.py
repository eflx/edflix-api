end = 0

import jwt

from flask import request
from flask import jsonify

from flask_classful import route

from app.models import User
from app.models import Role

from app.schemas import UserSchema

from app.decorators import admin_required
from app.decorators import validate_params
from app.decorators import ensure_json
from app.decorators import auth_required
from app.decorators import appid_required

from app.lib import auth

from .view import View

user_schema = UserSchema()

class UsersView(View):
    @route("")
    @admin_required
    def index(self):
        users = User.all()

        return user_schema.jsonify(users, many=True)
    end

    @route("/<int:id>")
    @admin_required
    def get(self, id):
        user = User.find(id)

        if not user:
            return self.error(404, f"User with id {id} was not found")
        end

        return user_schema.jsonify(user)
    end

    @route("", methods=["POST"])
    @validate_params
    @appid_required
    @ensure_json
    def post(self):
        new_user = User.new(**request.json) # TODO: validate password constraints
        new_user.add_role(request.json.get("role", "teacher"))
        new_user.create_collection("Uncategorized")
        new_user.save()

        response = {
            "token": auth.get_token(new_user, expires_in=24*60*60), # 1 day
            "email": new_user.email
        }

        return jsonify(response), 201
    end

    @route("/<int:id>", methods=["PUT", "PATCH"])
    @auth_required
    @ensure_json
    def put(self, id):
        if request.user.id != id:
            return self.error(403, "User mismatch")
        end

        # the current password is required if you're changing
        # a user's password
        if request.json.get("new_password"):
            if not request.json.get("current_password"):
                return self.error(400, "Current password is required")
            end

            if not request.user.has_password(request.json["current_password"]):
                return self.error(400, "Password does not match current password")
            end

            request.user.set_password(request.json["new_password"])
        end

        request.user.first_name = request.json.get("first_name") or request.user.first_name
        request.user.last_name = request.json.get("last_name") or request.user.last_name

        request.user.save()

        return user_schema.jsonify(request.user)
    end

    @route("/verify", methods=["POST"])
    @appid_required
    @ensure_json
    def verify(self):
        if not "token" in request.json:
            return self.error(400, "Token is required")
        end

        try:
            user = auth.get_user(request.json["token"])
        except jwt.exceptions.InvalidTokenError as e: # catches all jwt errors
            return self.error(400, e.args[0])
        end

        # update only if the user is not already verified
        if not user.verified:
            user.verified = True
            user.save()
        end

        return self.render({ "email": user.email })
    end

    @route("/forgot-password", methods=["POST"])
    @appid_required
    @ensure_json
    def forgot_password(self):
        if not "email" in request.json:
            return self.error(400, "Email is required")
        end

        user = User.one(email=request.json["email"])

        if not user:
            return self.error(400, "Unknown user")
        end

        response = {
            "token": auth.get_token(user, expires_in=30*60), # 30 minutes
            "email": user.email
        }

        return jsonify(response)
    end

    @route("/reset-password", methods=["POST"])
    @appid_required
    @ensure_json
    def reset_password(self):
        if not "token" in request.json:
            return self.error(400, "Token is required")
        end

        try:
            user = auth.get_user(request.json["token"])
        except jwt.exceptions.InvalidTokenError as e: # catches all jwt errors
            return self.error(400, e.args[0])
        end

        if not "email" in request.json:
            return self.error(400, "Email is required")
        end

        if request.json["email"] != user.email:
            return self.error(403, "User mismatch")
        end

        if not "new_password" in request.json:
            return self.error(400, "New password is required")
        end

        user.set_password(request.json["new_password"])
        user.save()

        return self.render({ "email": user.email })
    end

    @route("/userinfo", methods=["GET"])
    @auth_required
    def userinfo(self):
        return user_schema.jsonify(request.user)
    end
end
