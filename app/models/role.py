end = 0

from .model import Model, db

class Role(Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"Role ({self.name})"
    end
end
