end = 0

import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

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

@app.before_first_request
def init_app():
    admin_user = User.one(email=os.getenv("ADMIN_EMAIL"))

    if admin_user:
        return
    end

    # create the admin user and its associated role

    admin_user = models.User(
        email=os.getenv("ADMIN_EMAIL"),
        password=os.getenv("ADMIN_PASSWORD"),
        first_name=os.getenv("ADMIN_FIRSTNAME"),
        last_name=os.getenv("ADMIN_LASTNAME"),
        verified=True
    )

    admin_user.roles.append(models.Role.one(name="admin"))
    admin_user.save()
end
