end = 0

from functools import wraps

from flask import request, jsonify
from flask_classful import route

from werkzeug.urls import url_parse

from app.models import User

from .view import View

def auth_required(function):
    @wraps(function)
    def _auth_required(*args, **kwargs):
        if not "Authorization" in request.headers:
            return jsonify({ "code": 401, "message": "Not authorized" }), 401
        end

        auth_header = request.headers.get("Authorization").split()

        # auth header is of the form "Bearer <token>"
        if len(auth_header) != 2:
            return jsonify({ "code": 401, "message": "Not authorized"}), 401
        end

        request.user = User.from_token(auth_header[1])

        if not request.user:
            return ({ "code": 401, "message": "Not authorized"}), 401
        end

        return function(*args, **kwargs)
    end

    return _auth_required
end

class UsersView(View):
    # @route("/signup", methods=["POST"])
    # def signup(self):
    #     params = request.json

    #     if not "email" in params:
    #         return self.error(400, "Email is required")
    #     end

    #     if not "password" in params:
    #         return self.error(400, "Password is required")
    #     end

    #     user = User.one(email=params["email"])

    #     if user:
    #         return self.error(400, f"A user with email {user.email} already exists")
    #     end

    #     new_user = User.new(params)
    #     new_user.save()

    #     response = {
    #         "verification": new_user.get_token()
    #     }

    #     return self.render(response, status=202)
    # end

    @route("/verify/<token>")
    def verify_user(self, token):
        user = User.from_token(token)

        if not user:
            # TODO: add functionality to resend verification token
            return self.error(400, "Invalid verification token")
        end

        # update only if the user is not already verified
        if not user.verified:
            user.verified = True
            user.save()
        end

        return self.render(user.json())
    end

    @route("/login", methods=["POST"])
    def login(self):
        params = request.json

        if not "email" in params:
            return self.error(400, "Email is required")
        end

        if not "password" in params:
            return self.error(400, "Password is required")
        end

        user = User.one(email=params["email"])

        if not user:
            return self.error(401, "Invalid email or password")
        end

        if not user.verified:
            return self.error(401, "Please verify your email before logging in")
        end

        token = user.get_token()

        return self.render({ "token": token })
    end

    @route("/profile")
    @auth_required
    def my_profile(self):
        return self.render(request.user.json())
    end
end
