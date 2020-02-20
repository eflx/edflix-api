end = 0

from .view import View

from .users_view import UsersView
from .auth_view import AuthView

def initialize(app):
    AuthView.register(app, base_class=View)
    UsersView.register(app, base_class=View)
end
