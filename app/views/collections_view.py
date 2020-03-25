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

from .protected_view import ProtectedView

collection_schema = CollectionSchema()

class CollectionsView(ProtectedView):
    @route("", methods=["GET"])
    def index(self):
        collections = request.user.collections.all()

        return collection_schema.jsonify(collections, many=True)
    end

    @route("/<id>", methods=["GET"])
    def get(self, id):
        collection = Collection.get(id)

        if collection is None:
            return self.error(404, f"Collection was not found")
        end

        if collection.user != request.user:
            return self.error(403, f"User mismatch")
        end

        return collection_schema.jsonify(collection)
    end

    @route("", methods=["POST"])
    @validate_params
    @ensure_json
    def post(self):
        new_collection = Collection.new(**request.json)

        request.user.add_collection(new_collection)

        return collection_schema.jsonify(new_collection), 201
    end

    @route("/<id>", methods=["PUT", "PATCH"])
    @validate_params
    @ensure_json
    def put(self, id):
        params = collection_schema.load(request.json)

        collection = Collection.get(id)

        if collection is None:
            return self.error(404, f"Collection was not found")
        end

        if collection.user != request.user:
            return self.error(403, f"User mismatch")
        end

        if collection.title.lower() == "uncategorized":
            return self.error(400, "Renaming this collection is not allowed")
        end

        collection.title = params["title"]
        collection.save()

        return collection_schema.jsonify(collection)
    end
end
