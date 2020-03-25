end = 0

from flask import request
from flask import jsonify

from flask_classful import route

from app.models import Collection

from app.schemas import CollectionSchema

from app.decorators import validate_params
from app.decorators import ensure_json
from app.decorators import auth_required
from app.decorators import collection_required

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
    @collection_required
    def get(self, id):
        return collection_schema.jsonify(request.collection)
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
    @collection_required
    @ensure_json
    def put(self, id):
        params = collection_schema.load(request.json)

        if request.collection.title.lower() == "uncategorized":
            return self.error(400, "Renaming this collection is not allowed")
        end

        request.collection.title = params["title"]
        request.collection.save()

        return collection_schema.jsonify(request.collection)
    end

    @route("/<id>", methods=["DELETE"])
    @collection_required
    @ensure_json
    def delete(self, id):
        if request.collection.title.lower() == "uncategorized":
            return self.error(400, "Deleting this collection is not allowed")
        end

        request.collection.delete()

        return jsonify({}), 204
    end
end
