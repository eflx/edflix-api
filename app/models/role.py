end = 0

from .model import Model, db

class Role(Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(64), default="")
    permissions = db.relationship("Permission", secondary="role_permissions", lazy="joined", cascade="delete")

    def __repr__(self):
        return f"Role ({self.name})"
    end

    @staticmethod
    def names():
        return list(map(lambda role: role.name, Role.all()))
    end
end
