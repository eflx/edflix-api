end = 0

import os
import pytest

from app.models import User

def test_signup_existing_teacher(api):
    teacher_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert("exists" in response["message"])
end

required_fields_for_teacher_signup = ["first_name", "last_name", "email", "password", "application_id"]

@pytest.mark.parametrize("required_field", required_fields_for_teacher_signup)
def test_signup_teacher_with_missing_required_field(api, required_field):
    teacher_data = {
        "first_name": "Severus",
        "last_name": "Snape",
        "email": "severus.snape@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "application_id": os.getenv("APPLICATION_ID")
    }

    del teacher_data[required_field]

    error, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"])
end

def test_signup_new_teacher(api):
    teacher_data = {
        "first_name": "Pomona",
        "last_name": "Sprout",
        "email": "pomona.sprout@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users", data=teacher_data)

    user = User.one(email="pomona.sprout@hogwarts.edu")

    assert(status == 201)
    assert("token" in response)
    assert("email" in response)
    assert(response["email"] == "pomona.sprout@hogwarts.edu")
    assert(user.is_teacher())
    assert(len(user.collections.all()) == 1)
    assert(user.has_collection("Uncategorized"))
end

def test_signup_new_teacher_with_subjects(api):
    teacher_data = {
        "first_name": "Cuthbert",
        "last_name": "Binns",
        "email": "cuthbert.binns@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "subjects": ["Goblin Rebellions", "", "Giant Wars"], # TODO: Add None
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users", data=teacher_data)

    user = User.one(email="cuthbert.binns@hogwarts.edu")

    assert(status == 201)
    assert("token" in response)
    assert("email" in response)
    assert(response["email"] == "cuthbert.binns@hogwarts.edu")
    assert(user.is_teacher())
    assert(len(user.collections.all()) == 3)
    assert(user.has_collection("Uncategorized"))
    assert(user.has_collection("Goblin Rebellions"))
    assert(user.has_collection("Giant Wars"))
end

def test_signup_new_teacher_with_duplicate_subjects(api):
    teacher_data = {
        "first_name": "Alastor",
        "last_name": "Moody",
        "email": "alastor.moody@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "subjects": ["Uncategorized", "Aurors", "Dark Arts", "Aurors", "Uncategorized", "Curses"],
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users", data=teacher_data)

    user = User.one(email="alastor.moody@hogwarts.edu")

    assert(status == 201)
    assert("token" in response)
    assert("email" in response)
    assert(response["email"] == "alastor.moody@hogwarts.edu")
    assert(user.is_teacher())
    assert(len(user.collections.all()) == 4)
    assert(user.has_collection("Uncategorized"))
    assert(user.has_collection("Aurors"))
    assert(user.has_collection("Dark Arts"))
    assert(user.has_collection("Curses"))
end
