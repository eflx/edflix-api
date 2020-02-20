end = 0

from .schema import Schema, ma

from marshmallow import validate
from marshmallow import validates_schema
from marshmallow import ValidationError

class AuthSchema(Schema):
    email = ma.Str(
        required=True,
        validate=[
            validate.Email(error="Email address must be of the form user@host")
        ],
        error_messages={ "required": "Email is required" }
    )

    password = ma.Str(
        required=True,
        load_only=True,
        error_messages={ "required": "Password is required" }
    )
end
