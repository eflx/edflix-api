end = 0

from flask import url_for

from .schema import Schema, ValidationError

class UserSchema(Schema):
    def __init__(self, many=False):
        Schema.__init__(self, many)
    end

    def validate(self, params):
        self.validate_required(params, "first_name", "First name is required")
        self.validate_required(params, "last_name", "Last name is required")
        self.validate_required(params, "email", "Email is required")
        self.validate_required(params, "password", "Password is required")

        return \
        {
            "first_name": params["first_name"],
            "last_name": params["last_name"],
            "email": params["email"],
            "password": params["password"]
        }
    end

    def transform(self, user):
        return \
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
            "url": url_for("UsersView:get", id=user.id)
        }
    end
end

user_schema = UserSchema()
users_schema = UserSchema(many=True)
