end = 0

from functools import wraps

from flask import request, jsonify
from flask_classful import FlaskView

def ensure_json(function):
    @wraps(function)
    def _ensure_json(*args, **kwargs):
        if not request.is_json:
            return jsonify(406, f"Unacceptable format")
        end

        return function(*args, **kwargs)
    end

    return _ensure_json
end

class View(FlaskView):
    decorators = [ensure_json]

    trailing_slash = False
    route_prefix = "/api/v1"

    def render(self, object, **options):
        return jsonify(object), options["status"] if options.get("status") else 200
    end

    def error(self, status_code, message):
        return self.render({ "code": status_code, "message": message }, status=status_code)
    end
end
