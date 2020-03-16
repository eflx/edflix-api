end = 0

import os
import sys

sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv(verbose=True)

import pytest

from app import create_app
from app import db as database
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
def db():
    database.create_all()

    teacher_role = Role(name="teacher")
    admin_role = Role(name="admin")
    school_admin_role = Role(name="school-admin")

    for role in [teacher_role, admin_role, school_admin_role]:
        role.save()
    end

    # create all verified users so logging them in won't return an 403,
    # but create one unverified that we can use to test logging in
    # an unverified user
    dumbledore = User(first_name="Albus", last_name="Dumbledore", password="P@55w0rd", email="albus.dumbledore@hogwarts.edu", verified=True)
    mcgonagall = User(first_name="Minerva", last_name="McGonagall", password="P@55w0rd", email="minerva.mcgonagall@hogwarts.edu", verified=True)
    flitwick = User(first_name="Filius", last_name="Flitwick", password="P@55w0rd", email="filius.flitwick@hogwarts.edu", verified=True)
    lockhart = User(first_name="Gilderoy", last_name="Lockhart", password="P@55w0rd", email="gilderoy.lockhart@hogwarts.edu", verified=False)

    for teacher in [dumbledore, mcgonagall, flitwick, lockhart]:
        teacher.roles.append(teacher_role)
    end

    dumbledore.roles.append(school_admin_role)

    for teacher in [dumbledore, mcgonagall, flitwick, lockhart]:
        teacher.save()
    end

    yield database

    database.drop_all()
end

@pytest.fixture(scope="module")
def api(test_client, db):
    return API(test_client)
end

@pytest.fixture(scope="function")
def auth(api):
    auth_response, _ = api.post("auth/token", data={ "email": "albus.dumbledore@hogwarts.edu", "password": "P@55w0rd" })

    return auth_response
end

@pytest.fixture(scope="function")
def auth_header(auth):
    return { "Authorization": f"Bearer {auth['token']}" }
end

@pytest.fixture(scope="module")
def user(test_client, db):
    user = User.one(email="minerva.mcgonagall@hogwarts.edu")

    return user
end
