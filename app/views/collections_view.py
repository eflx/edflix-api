end = 0

from flask import request
from flask import jsonify

from flask_classful import route

from app.models import Collection

from app.schemas import CollectionSchema

from app.decorators import validate_params
from app.decorators import ensure_json
from app.decorators import auth_required

from app.lib import auth

from .authenticated_view import AuthenticatedView

collection_schema = CollectionSchema()

class CollectionsView(AuthenticatedView):
    @route("", methods=["GET"])
    def index(self):
        collections = request.user.collections.all()

        return collection_schema.jsonify(collections, many=True)
    end

    @route("", methods=["POST"])
    @ensure_json
    def post(self):
        if not "title" in request.json:
            return self.error(400, "Title is required")
        end

        title = request.json["title"]

        if not title or title.lower() == "uncategorized":
            return self.error(400, f"Title '{title}' is not allowed")
        end

        new_collection = Collection.new(**request.json)

        request.user.add_collection(new_collection)

        return collection_schema.jsonify(new_collection), 201
    end
end
