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
    @route("")
    def index(self):
        collections = request.user.collections.all()

        return collection_schema.jsonify(collections, many=True)
    end
end
