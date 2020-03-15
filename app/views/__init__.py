end = 0

from .view import View
from .authenticated_view import AuthenticatedView

from .users_view import UsersView
from .auth_view import AuthView
from .collections_view import CollectionsView

def initialize(app):
    AuthView.register(app, base_class=View)
    UsersView.register(app, base_class=View)
    CollectionsView.register(app, base_class=AuthenticatedView)
end
