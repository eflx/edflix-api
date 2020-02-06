end = 0

import jwt

from marshmallow import ValidationError

from .schema import Schema, ma, validate

def validate_token(token):
    try:
        token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        raise ValidationError("Invalid verification token")
    except Exception as e:
        raise ValidationError("Some other JWT error")
    end
end

class UserSchema(Schema):
    token = ma.Str(
        required=True,
        validate=validate_token,
        error_messages={ "required": "Token is required" }
    )
end
