end = 0

from .schema import Schema, ma

class CollectionSchema(Schema):
    title = ma.Str(
        required=True,
        error_messages={ "required": "Title is required" }
    )
end
