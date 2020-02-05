end = 0

from .schema import Schema, ma, validate

class UserSchema(Schema):
    url = ma.URLFor("UsersView:get", id="<id>")

    first_name = ma.Str(
        required=True,
        error_messages={ "required": "First name is required" }
    )

    last_name = ma.Str(
        required=True,
        error_messages={ "required": "Last name is required" }
    )

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

    subjects = ma.Str(load_only=True)

    role = ma.Str(
        required=True,
        load_only=True,
        validate=validate.OneOf(["teacher"], error="Role must be 'teacher'"),
        error_messages={
            "required": "Role is required"
        }
    )

    application_id = ma.Str(
        required=True,
        load_only=True,
        error_messages={ "required": "Application id is required" }
    )
end
