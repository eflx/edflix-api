from .user import user_schema, users_schema
from .auth import auth_schema

schemas = {
    "User": user_schema,
    "Auth": auth_schema
}
