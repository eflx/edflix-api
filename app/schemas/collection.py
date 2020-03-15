end = 0

from .schema import Schema, ma

class CollectionSchema(Schema):
    __envelope__ = "collections"

    title = ma.Str(
        required=True,
        error_messages={ "required": "Title is required" }
    )
end
