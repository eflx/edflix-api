end = 0

from .model import Model, db

class Permission(Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(64), default="")

    def __repr__(self):
        return f"Permission ({self.name})"
    end
end
