end = 0

import jwt

from flask import request
from flask import jsonify

from flask_classful import route

from app.models import User
from app.schemas import UserSchema

from app.decorators import admin_required
from app.decorators import validate_params
from app.decorators import ensure_json

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
    @ensure_json
    def post(self):
        # TODO: check application id to see if it is allowed

        new_user = User.new(request.json)
        new_user.role = Role.get(request.json["role"])
        new_user.save()

        response = {
            # expires in one day
            "token": new_user.get_token(expires_in=24*60*60)
        }

        return jsonify(response), 202
    end

    @route("/verify", methods=["POST"])
    def verify(self):
        if not "token" in request.params:
            return self.error(400, "Token is required")
        end

        try:
            user = User.from_token(request.params["token"])
        except jwt.exceptions.InvalidTokenError as e: # catches all jwt errors
            return self.error(400, e.args[0])
        end

        # update only if the user is not already verified
        if not user.verified:
            user.verified = True
            user.save()
        end

        return self.render(user_schema.dump(user))
    end

    # @route("/login", methods=["POST"])
    # def login(self):
    #     params = request.json

    #     if not "email" in params:
    #         return self.error(400, "Email is required")
    #     end

    #     if not "password" in params:
    #         return self.error(400, "Password is required")
    #     end

    #     user = User.one(email=params["email"])

    #     if not user:
    #         return self.error(401, "Invalid email or password")
    #     end

    #     if not user.verified:
    #         return self.error(401, "Please verify your email before logging in")
    #     end

    #     token = user.get_token()

    #     return self.render({ "token": token })
    # end

    # @route("/profile")
    # @auth_required
    # def my_profile(self):
    #     return self.render(request.user.json())
    # end
end
