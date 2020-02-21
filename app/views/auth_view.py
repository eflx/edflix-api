end = 0

import os

from app.models import User

from flask import make_response
from flask import request
from flask import jsonify

from flask_classful import route

from app.schemas import AuthSchema
from app.schemas import UserSchema

from app.decorators import validate_params
from app.decorators import ensure_json

from .view import View

auth_schema = AuthSchema()
user_schema = UserSchema()

class AuthView(View):
    @route("/token", methods=["POST"])
    @validate_params
    @ensure_json
    def token(self):
        auth_params = auth_schema.load(request.json)

        user = User.authenticate(auth_params)

        if not user:
            return self.error(400, "The email or password is incorrect")
        end

        response = {
            "token": user.get_auth_token()
        }

        return jsonify(response), 200
    end
end
