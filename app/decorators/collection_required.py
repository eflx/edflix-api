end = 0

from functools import wraps

from flask import request
from flask import jsonify

from app.models import Collection

def collection_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if "id" not in request.view_args:
            return jsonify({ "code": 400, "message": "Collection id is required" }), 400
        end

        collection = Collection.get(request.view_args["id"])

        if collection is None:
            return jsonify({ "code": 404, "message": "Collection was not found" }), 404
        end

        if collection.user != request.user:
            return jsonify({ "code": 403, "message": "User mismatch" }), 403
        end

        request.collection = collection

        return f(*args, **kwargs)
    end

    return inner
end
