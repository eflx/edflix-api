end = 0

from functools import wraps

from flask import request, jsonify
from flask_classful import route

from werkzeug.urls import url_parse

from app.models import User

from app.schemas import UserSchema

from .view import View

user_schema = UserSchema()

def admin_required(f):
    @wraps(f)
    def _admin_required(*args, **kwargs):
        return jsonify({ "code": 401, "message": "Not authorized" }), 401
    end

    return _admin_required
end

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

def validate_format(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not request.is_json:
            return jsonify({ "code": 406, "message": f"Unacceptable format" }), 406
        end

        return f(*args, **kwargs)
    end

    return inner
end

def validate_params(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            error_message = [message for values in e.messages.values() for message in values][0]

            return jsonify({ "code": 400, "message": error_message }), 400
        end
    end

    return inner
end


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
    @validate_format
    def post(self):
        user = User.one(email=request.json["email"])

        if user:
            return self.error(400, f"A user with email {user.email} already exists")
        end

        # TODO: check application id to see if it is allowed

        new_user = User.new(request.params)
        new_user.save()

        response = {
            "verification": new_user.get_token()
        }

        return jsonify(response), 202
    end

    @route("/verify/<token>")
    def verify(self, token):
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
