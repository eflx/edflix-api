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

        role = Role.one(name=request.json.get("role", "teacher"))

        new_user = User.new(request.json)
        new_user.roles.append(role)
        new_user.save()

        response = {
            # expires in one day
            "token": new_user.get_verification_token(expires_in=24*60*60),
            "email": new_user.email,
            "roles": list(map(lambda role: role.name, new_user.roles))
        }

        return jsonify(response), 202
    end

    @route("/verify", methods=["POST"])
    @ensure_json
    def verify(self):
        if not "token" in request.json:
            return self.error(400, "Token is required")
        end

        try:
            user = User.from_token(request.json["token"])
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
end
