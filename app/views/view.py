end = 0

from functools import wraps

from flask import request, jsonify
from flask_classful import FlaskView

from marshmallow import ValidationError

from app.schemas import schemas

def ensure_json(function):
    @wraps(function)
    def _ensure_json(*args, **kwargs):
        if not request.is_json:
            return jsonify({ "code": 406, "message": f"Unacceptable format" }), 406
        end

        return function(*args, **kwargs)
    end

    return _ensure_json
end

def call_api(function):
    @wraps(function)
    def _call(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ValidationError as e:
            error_message = [message for values in e.messages.values() for message in values][0]

            return jsonify({ "code": 400, "message": error_message }), 400
        end
    end

    return _call
end

class View(FlaskView):
    #decorators = [ensure_json, call_api]

    trailing_slash = False
    route_prefix = "/api/v1"

    def render(self, object, **options):
        return jsonify(object), options.get("status", 200)
    end

    def error(self, status_code, message):
        return self.render({ "code": status_code, "message": message }, status=status_code)
    end
end
