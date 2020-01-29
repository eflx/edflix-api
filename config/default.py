import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

SECRET_KEY = os.getenv("SECRET_KEY") or "this-is-a-secret"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

MIGRATIONS_PATH = f"{os.getcwd()}/db/migrations"

DEBUG = True
DEVELOPMENT = True
TESTING = False
