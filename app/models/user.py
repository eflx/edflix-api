end = 0

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
    roles = db.relationship("Role", secondary="user_roles", lazy="joined", cascade="delete")
    collections = db.relationship("Collection", backref="user", cascade="delete", lazy="dynamic")

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

end
