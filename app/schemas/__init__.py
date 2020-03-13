from .user import UserSchema
from .collection import CollectionSchema
from .auth import AuthSchema

schemas = {
    "User": UserSchema(),
    "Collection": CollectionSchema()
}
