end = 0

from functools import wraps

from flask import request
from flask import jsonify

from marshmallow import ValidationError

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
