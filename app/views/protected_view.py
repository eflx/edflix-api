end = 0

from .view import View

from app.decorators import auth_required

class ProtectedView(View):
    decorators = [auth_required]
end
