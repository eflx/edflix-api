end = 0

from .view import View

from .users_view import UsersView

def initialize(app):
    UsersView.register(app, base_class=View)
end
