end = 0

from functools import wraps

from flask import request
from flask import jsonify

from app.lib import auth

def auth_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not "Authorization" in request.headers:
            return jsonify({ "code": 401, "message": "Not authorized" }), 401
        end

        auth_header = request.headers.get("Authorization").split()

        # auth header is of the form "Bearer <token>"
        if len(auth_header) != 2:
            return jsonify({ "code": 401, "message": "Not authorized" }), 401
        end

        request.user = auth.get_user(auth_header[1])

        if not request.user:
            return jsonify({ "code": 401, "message": "Not authorized" }), 401
        end

        return f(*args, **kwargs)
    end

    return inner
end
