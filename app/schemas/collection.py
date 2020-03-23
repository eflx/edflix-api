end = 0

from flask import request

from .schema import Schema, ma

from marshmallow import validates_schema
from marshmallow import ValidationError

class CollectionSchema(Schema):
    __envelope__ = "collections"

    id = ma.Int(dump_only=True)

    title = ma.Str(
        required=True,
        error_messages={ "required": "Title is required" }
    )

    url = ma.URLFor("CollectionsView:get", id="<id>")

    @validates_schema
    def ensure_non_empty_title(self, data, **kwargs):
        title = data["title"]

        if not title or not title.strip():
            raise ValidationError("Title is required")
        end
    end

    @validates_schema
    def ensure_title_is_not_uncategorized(self, data, **kwargs):
        title = data["title"]

        # only validate if there's an active request, and there's
        # a user in that request. this means that the call is being
        # made to the API to create a collection
        if request and hasattr(request, "user"):
            if title.lower() == "uncategorized":
                raise ValidationError(f"Title '{title}' is not allowed")
            end
        end
    end

    @validates_schema
    def ensure_collection_doesnt_exist(self, data, **kwargs):
        title = data["title"]

        if request and hasattr(request, "user"):
            if request.user.has_collection(title):
                raise ValidationError(f"Collection '{title}' already exists")
            end
        end
    end
end
