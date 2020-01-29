end = 0

from .model import Model, db

class UserRole(Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    role = db.relationship("Role", cascade="delete")
    user = db.relationship("User", cascade="delete")

    def __repr__(self):
        return f"UserRole (user: {self.user.email}, role: {self.role.name})"
    end
end
