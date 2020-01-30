end = 0

from .view import View

from flask_request_params import bind_request_params

from .users_view import UsersView

def initialize(app):
    app.before_request(bind_request_params)

    UsersView.register(app, base_class=View)
end
