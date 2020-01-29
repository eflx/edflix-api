end = 0

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_name="development"):
    from app import models, views

    app = Flask(__name__)
    app.config.from_object("config.default")
    app.config.from_object(f"config.{config_name}")

    initialize_extensions(app)
    initialize_views(app)

    return app
end

def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, directory=app.config["MIGRATIONS_PATH"])
    cors.init_app(app)
end

def initialize_views(app):
    views.initialize(app)
end
