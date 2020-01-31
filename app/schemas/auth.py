end = 0

from flask import url_for

from .schema import Schema, ValidationError

class AuthSchema(Schema):
    def __init__(self, many=False):
        Schema.__init__(self, many)
    end

    def validate(self, params):
        self.validate_required(params, "first_name", "First name is required")
        self.validate_required(params, "last_name", "Last name is required")
        self.validate_required(params, "email", "Email is required")
        self.validate_required(params, "password", "Password is required")
        self.validate_required(params, "application_key", "Application key is required")

        return {
            "first_name": params["first_name"],
            "last_name": params["last_name"],
            "email": params["email"],
            "password": params["password"],
            "subjects": params.get("subjects", []),
            "role": params.get("role", "teacher"),
            "application_key": params["application_key"]
        }
    end

    def transform(self, params):
        raise NotImplementedError()
    end
end

auth_schema = AuthSchema()
