end = 0

from functools import wraps

from flask import jsonify

# no admins yet, so this decorator always returns 401 Unauthorized
def admin_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        return jsonify({ "code": 401, "message": "Unauthorized" }), 401
    end

    return inner
end
