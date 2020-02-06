end = 0

from functools import wraps

from flask import jsonify
from flask import request

def ensure_json(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not request.is_json:
            return jsonify({ "code": 406, "message": f"Unacceptable format" }), 406
        end

        return f(*args, **kwargs)
    end

    return inner
end
