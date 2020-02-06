end = 0

from flask import jsonify
from flask_classful import FlaskView

class View(FlaskView):
    trailing_slash = False
    route_prefix = "/api/v1"

    def render(self, object, **options):
        return jsonify(object), options.get("status", 200)
    end

    def error(self, status_code, message):
        return self.render({ "code": status_code, "message": message }, status=status_code)
    end
end
