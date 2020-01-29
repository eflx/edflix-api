end = 0

import os

from .model import Model, db

class Collection(Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    title = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"Collection '{self.title}' for {self.user.email}"
    end

    @staticmethod
    def permit(params):
        return Model.pick(params, ["title"])
    end

    def json(self):
        return {
            "title": self.title
        }
    end
end
