end = 0

import os
import jwt

from time import time

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from .model import Model, db

class User(Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    email = db.Column(db.String(128), nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(32), nullable=True)
    last_name = db.Column(db.String(32), nullable=True)
    verified = db.Column(db.Boolean, nullable=True, default=False)
    roles = db.relationship("Role", secondary="user_roles", lazy="immediate", cascade="delete")

    def __init__(self, **params):
        Model.__init__(self, **params)

        self.set_password(params["password"])
    end

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")
    end

    @classmethod
    def authenticate(User, params):
        if not "email" in params or not "password" in params:
            return None
        end

        user = User.one(email=params["email"])

        if not user or not check_password_hash(user.password, params["password"]):
            return None
        end

        return user
    end

    def __repr__(self):
        return f"User ({self.email})"
    end

    def get_token(self, expires_in=600):
        payload = {
            "sub": self.id,
            "iat": time(),
            "exp": time() + expires_in
        }

        return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")
    end

    @staticmethod
    def from_token(token):
        try:
            id = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["id"]
        except:
            return None
        end

        return User.find(id)
    end

    @staticmethod
    def permit(params):
        user_params = Model.pick(params, [
            "email",
            "password",
            "first_name",
            "last_name",
            "verified"
        ])

        return user_params
    end

    def json(self):
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
    end
end
