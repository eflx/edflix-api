end = 0

from .model import Model, db

class RolePermission(Model):
    __tablename__ = "role_permissions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"))

    role = db.relationship("Role", cascade="delete")
    permission = db.relationship("Permission", cascade="delete")

    def __repr__(self):
        return f"RolePermission (role: {self.role.name}, permission: {self.permission.name})"
    end
end
