end = 0

import os

from app.models import User

from flask import make_response
from flask import request
from flask import jsonify

from flask_classful import route

from app.schemas import AuthSchema

auth_schema = AuthSchema()

from .view import View

class AuthView(View):
    @route("/token", methods=["POST"])
    def token(self):
        auth_params = auth_schema.load(request.json)

        user = User.authenticate(auth_params)

        if not user:
            return self.error(400, "The email or password is incorrect")
        end

        token = user.get_auth_token()

        response = make_response({}, 200)
        response.headers["Authorization"] = f"Bearer {token}"

        return response
    end
end
