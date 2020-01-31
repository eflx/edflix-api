end = 0

from .view import View

from flask_request_params import Params, bind_request_params

def __contains__(params, key):
    return key in params._params
end

def __getattr__(params, key):
    return params._params.get(key)
end

Params.__contains__ = __contains__
Params.__getattr__ = __getattr__

from .users_view import UsersView
from .auth_view import AuthView

def initialize(app):
    app.before_request(bind_request_params)

    AuthView.register(app, base_class=View)
    UsersView.register(app, base_class=View)
end
