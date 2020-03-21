end = 0

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from .model import Model, db

from .collection import Collection
from .role import Role

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

    def __repr__(self):
        return f"User ({self.email})"
    end

    def has_password(self, password):
        return check_password_hash(self.password, password)
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

        if not user or not user.has_password(params["password"]):
            return None
        end

        return user
    end

    def role_names(self):
        return list(map(lambda role: role.name, self.roles))
    end

    def has_role(self, role_name):
        return role_name in self.role_names()
    end

    def add_role(self, role_name):
        if self.has_role(role_name):
            return
        end

        default_role = Role.one(name="teacher")

        role = Role.one(name=role_name) or default_role

        self.roles.append(role)
        self.save()
    end

    def is_teacher(self):
        return self.has_role("teacher")
    end

    def has_collection(self, title):
        return title.lower() in map(lambda collection: collection.title.lower(), self.collections)
    end

    def create_collection(self, title):
        new_collection = Collection.new(title=title)

        return self.add_collection(new_collection)
    end

    def add_collection(self, collection):
        collection.user = self

        # can save a collection only if the owner
        # has an id (i.e., is already saved)
        collection.save() if self.id else None

        return collection
    end
end
