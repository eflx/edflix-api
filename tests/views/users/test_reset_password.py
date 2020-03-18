end = 0

import os
import jwt
import pytest

from time import time

required_fields_for_password_reset = ["token", "email", "application_id", "new_password"]

@pytest.mark.parametrize("required_field", required_fields_for_password_reset)
def test_password_reset_with_missing_required_field(api, required_field):
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 30 mins for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    password_reset_data = {
        "token": token,
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    del password_reset_data[required_field]

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"] or "token" in error["message"].lower())
end

def test_password_reset_with_invalid_token(api):
    password_reset_data = {
        "token": "dummy-token",
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 400)
    assert(error["code"] == 400)
end

def test_password_reset_with_invalid_application_id(api):
    password_reset_data = {
        "token": "does-not-matter",
        "application_id": "unknown-application",
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("unknown" in error["message"].lower())
end

# testing resetting password for a user that's not identified by the
# token
def test_password_reset_for_another_user(api):
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 30 mins for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    password_reset_data = {
        "token": token,
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "filius_flitwick@hogwarts.edu", # can't do that!
        "new_password": "newpassword"
    }

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 403)
    assert(error["code"] == 403)
    assert("mismatch" in error["message"])
end

def test_password_reset_with_valid_input(api):
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 30 mins for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    password_reset_data = {
        "token": token,
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    response, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 200)
    assert("email" in response)
    assert(response["email"] == "albus.dumbledore@hogwarts.edu")
end
