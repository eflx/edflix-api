end = 0

import os
import sys

sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv(verbose=True)

import pytest

from app import create_app
from app import db
from app.models import User, Role

from tests.api import API

@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")

    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()
end

@pytest.fixture(scope="module")
def init_db():
    db.create_all()

    teacher_role = Role(name="teacher")
    admin_role = Role(name="admin")
    school_admin_role = Role(name="school-admin")

    for role in [teacher_role, admin_role, school_admin_role]:
        role.save()
    end

    dumbledore = User(first_name="Albus", last_name="Dumbledore", password="P@55w0rd", email="albus.dumbledore@hogwarts.edu")
    mcgonagall = User(first_name="Minerva", last_name="McGonagall", password="P@55w0rd", email="minerva.mcgonagall@hogwarts.edu")
    flitwick = User(first_name="Filius", last_name="Flitwick", password="P@55w0rd", email="filius.flitwick@hogwarts.edu")

    for teacher in [dumbledore, mcgonagall, flitwick]:
        teacher.roles.append(teacher_role)
    end

    for teacher in [dumbledore, mcgonagall, flitwick]:
        teacher.save()
    end

    yield db

    db.drop_all()
end

@pytest.fixture(scope="module")
def api(test_client, init_db):
    return API(test_client)
end

@pytest.fixture(scope="function")
def auth(api, init_db):
    user_data, status = api.post("auth/login", data={ "email": "frizzy@me.com", "password": "P@55w0rd" })

    yield user_data
end
