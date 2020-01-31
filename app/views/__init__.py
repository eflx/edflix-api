end = 0

from .view import View

from flask_request_params import Params, bind_request_params

Params.__contains__ = lambda params, key: key in params._params

from .users_view import UsersView
from .auth_view import AuthView

def initialize(app):
    app.before_request(bind_request_params)

    AuthView.register(app, base_class=View)
    UsersView.register(app, base_class=View)
end
