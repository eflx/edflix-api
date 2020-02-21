end = 0

import os
import jwt
import pytest

from time import time

def test_get_all_users(api):
    error_data, status = api.get("users")

    assert(status == 401)
    assert(error_data["code"] == 401)
    assert("Unauthorized" in error_data["message"])
end

def test_get_one_user(api):
    error_data, status = api.get("users")

    assert(status == 401)
    assert(error_data["code"] == 401)
    assert("Unauthorized" in error_data["message"])
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

    response_data, status = api.post("users", data=teacher_data)

    assert(status == 202)
    assert("token" in response_data)
end

def test_signup_existing_teacher(api):
    teacher_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response_data, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert("exists" in response_data["message"])
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

    error_data, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert(error_data["code"] == 400)
    assert("required" in error_data["message"])
end

def test_signup_school_admin(api):
    admin_data = {
        "first_name": "Remus",
        "last_name": "Lupin",
        "email": "remus.lupin@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "school-admin",
        "school_name": "Hogwarts",
        "school_address": "Scotland",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response_data, status = api.post("users", data=admin_data)

    assert(status == 202)
    assert("token" in response_data)
end

required_fields_for_admin_signup = ["first_name", "last_name", "email", "password", "school_name", "school_address", "application_id"]

@pytest.mark.parametrize("required_field", required_fields_for_admin_signup)
def test_signup_school_admin_with_missing_required_field(api, required_field):
    admin_data = {
        "first_name": "Horace",
        "last_name": "Slughorn",
        "email": "horace.slughorn@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "school-admin",
        "school_name": "Hogwarts",
        "school_address": "Scotland",
        "application_id": os.getenv("APPLICATION_ID")
    }

    del admin_data[required_field]

    error_data, status = api.post("users", data=admin_data)

    assert(status == 400)
    assert(error_data["code"] == 400)
    assert("required" in error_data["message"])
end

def test_user_verification_without_token(api):
    data = {}

    error_data, status = api.post("users", data=data)

    assert(status == 400)
    assert("required" in error_data["message"])
end

def test_user_verification_with_valid_token(api):
    # test with dummy valid token -- all we're testing for
    # right now is that there *is* a token in the payload
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 24 hours for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    data = {
        "token": token
    }

    user_data, status = api.post("users/verify", data=data)

    assert(status == 200)
    assert(user_data.get("email") == "albus.dumbledore@hogwarts.edu")
end

def test_user_verification_with_invalid_token(api):
    data = {
        "token": "dummytoken"
    }

    user_data, status = api.post("users/verify", data=data)

    assert(status == 400)
end

def test_login(api):
    login_data = {
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd"
    }

    response, status = api.post("auth/token", data=login_data)

    assert(status == 200)
    assert("token" in response)

    try:
        token = jwt.decode(response["token"], os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError as e:
        token = None
    end

    assert(token is not None)
    assert("sub" in token)
    assert("iat" in token)
    assert("exp" in token)
    assert(int(token["exp"] - token["iat"]) == 10*24*60*60)
end

required_fields_for_login = ["email", "password"]

@pytest.mark.parametrize("required_field", required_fields_for_login)
def test_login_with_missing_fields(api, required_field):
    login_data = {
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd"
    }

    del login_data[required_field]

    error_data, status = api.post("auth/token", data=login_data)

    assert(status == 400)
    assert(error_data["code"] == 400)
    assert("required" in error_data["message"])
end

@pytest.mark.parametrize("required_field", required_fields_for_login)
def test_login_with_incorrect_credentials(api, required_field):
    login_data = {
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd"
    }

    # mess up the required field, turn it into an incorrect
    # value
    login_data[required_field] = login_data[required_field] + "x"

    error_data, status = api.post("auth/token", data=login_data)

    assert(status == 400)
    assert(error_data["code"] == 400)
    assert("incorrect" in error_data["message"])
end

def test_get_userinfo_without_token(api):
    error_data, status = api.get("users/userinfo")

    assert(status == 401)
    assert("Not authorized" in error_data["message"])
end

def test_get_userinfo_with_correct_token(api, auth):
    user_data, status = api.get("users/userinfo", headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 200)
    assert(user_data.get("email") == "albus.dumbledore@hogwarts.edu")
end
