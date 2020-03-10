end = 0

import os

from functools import wraps

from flask import request
from flask import jsonify

from app.lib import auth

# must appear before @ensure_json because it checks for the application id
# in request.json
def appid_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        known_applications = {
            os.getenv("APPLICATION_ID"): "EdFlix Flask"
        }

        if not "application_id" in request.json:
            return jsonify({ "code": 400, "message": "Application id is required" }), 400
        end

        # check for application id in the list of allowed application
        # ids to confirm this is a bona fide application. TODO: get this
        # from the list right now, but move it to the database later:

        # application = Application.one(id=request.json["application_id"])

        # if not application:
        #     return jsonify(400, "Unknown application"), 400
        # end

        if not request.json["application_id"] in known_applications:
            return jsonify({ "code": 400, "message": "Unknown application" }), 400
        end

        return f(*args, **kwargs)
    end

    return inner
end
